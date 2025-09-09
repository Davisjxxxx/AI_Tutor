# backend/coach.py
import os
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from pydantic import ValidationError
from typing import List, Dict
from sqlalchemy.orm import Session
import jwt

from backend.database import get_db, SessionLocal
from backend.models_coach import Project, Task, CheckIn, Recall, Streak
from backend.schemas_coach import (
    AMResponse, PMResponse, UnstickRequest, UnstickResponse, RecallQuiz
)

# --- Configuration & Router Setup ---
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
router = APIRouter(prefix="/api/coach", tags=["AI Coach"])


# --- Authentication Dependency ---
async def get_current_user_id(request: Request) -> str:
    """Dependency to get user_id from JWT in Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('user_id')
        if not user_id:
            raise HTTPException(status_code=401, detail="User not found in token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# --- LangChain / Retrieval Placeholders ---
def retrieve_snippets(user_id: str, query: str, k: int = 5) -> List[str]:
    """TODO: Call LangChain retriever over Chroma."""
    return []

def call_llm_am(tasks_json, yesterday_json, energy: int, snippets: List[str]) -> AMResponse:
    """TODO: Compose AM prompt, call LLM, parse JSON to AMResponse."""
    data = {
        "focus_project": {"id": tasks_json[0]["project_id"] if tasks_json else "P1", "reason": "Closest to revenue"},
        "top3_today": [
            {"task_id": (tasks_json[0]["id"] if tasks_json else "T1"), "title": "Implement login POST", "minutes": 25, "test": "curl 200"},
            {"task_id": (tasks_json[1]["id"] if len(tasks_json)>1 else "T2"), "title": "Write happy-path test", "minutes": 20},
            {"task_id": (tasks_json[2]["id"] if len(tasks_json)>2 else "T3"), "title": "Wire button", "minutes": 15}
        ],
        "timebox_plan": [
            {"task_id": "T1", "start_suggestion": "09:15", "minutes": 25},
            {"task_id": "T2", "start_suggestion": "10:00", "minutes": 20},
            {"task_id": "T3", "start_suggestion": "10:30", "minutes": 15},
        ],
        "study_slot": {"topic": "Flask sessions", "plan": "Read docs & add 1 test", "minutes": 15},
        "risk": "Context switching after 11am; protect 09:15–11:00."
    }
    return AMResponse(**data)

def call_llm_pm(today_context, snippets: List[str]) -> PMResponse:
    """TODO: Compose PM prompt, call LLM, parse JSON to PMResponse."""
    data = {
        "shipped": [{"title": "Login handler"}], "learned": ["Session cookies basics"],
        "blockers": [{"description": "Token leak logs", "next_step": "Redact before logging"}],
        "tomorrow_top3": [{"task_id": "T4", "title": "Add CSRF token", "minutes": 20}],
        "create_recalls": [{"q": "What is a session cookie?", "a": "Server-set cookie to maintain state."}],
        "coach_note": "Solid progress."
    }
    return PMResponse(**data)

def call_llm_unstick(req: UnstickRequest, snippets: List[str]) -> UnstickResponse:
    """TODO: Compose Rubber-Duck prompt, call LLM, parse JSON to UnstickResponse."""
    data = {
        "hypotheses": ["Missing session secret in config"],
        "minimal_repro": "pytest test_auth.py::test_login_sets_session_cookie",
        "smallest_change": "Set SECRET_KEY",
        "rollback_plan": "Revert config change"
    }
    return UnstickResponse(**data)


# --- Helper Functions ---
def _get_open_tasks(db: Session):
    q = db.query(Task).filter(Task.status != "done").order_by(Task.priority.desc()).limit(10)
    return [dict(
        id=t.id, project_id=t.project_id, title=t.title, detail=t.detail or "",
        status=t.status, priority=t.priority, due_date=str(t.due_date) if t.due_date else None,
        est_minutes=t.est_minutes
    ) for t in q.all()]

def _get_yesterday_pm(db: Session):
    c = db.query(CheckIn).filter(CheckIn.type=="PM").order_by(CheckIn.ts.desc()).first()
    if not c: return {}
    return dict(
        ts=c.ts.isoformat(), what_learned=c.what_learned, where_stuck=c.where_stuck,
        next_action=c.next_action, energy_1_5=c.energy_1_5
    )


# --- API Routes ---
# TODO: Add rate limiting (e.g., using slowapi)

@router.post("/am", response_model=AMResponse)
def coach_am(
    payload: Dict = Body(None),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    tasks = _get_open_tasks(db)
    yesterday = _get_yesterday_pm(db)
    snippets = retrieve_snippets(user_id, "AM planning: tasks + yesterday blockers", k=5)
    
    try:
        energy = int((payload or {}).get("energy", 4))
        resp = call_llm_am(tasks, yesterday, energy, snippets)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={"error": "AMResponse schema invalid", "details": e.errors()})

    ci = CheckIn(
        id=f"AM-{datetime.utcnow().isoformat()}", type="AM",
        next_action="; ".join([t.title for t in resp.top3_today]),
        energy_1_5=energy
    )
    db.add(ci)
    db.commit()
    return resp

@router.post("/pm", response_model=PMResponse)
def coach_pm(
    payload: Dict = Body(None),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    snippets = retrieve_snippets(user_id, "PM wrap: shipped/learned/blockers", k=5)
    try:
        resp = call_llm_pm(today_context={}, snippets=snippets)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail={"error": "PMResponse schema invalid", "details": e.errors()})

    ci = CheckIn(
        id=f"PM-{datetime.utcnow().isoformat()}", type="PM",
        what_learned="n".join(resp.learned),
        where_stuck="n".join([b.description for b in resp.blockers]),
        next_action="; ".join([t.title for t in resp.tomorrow_top3]),
        energy_1_5=(payload or {}).get("energy", 3)
    )
    db.add(ci)

    for i, r in enumerate(resp.create_recalls):
        db.add(Recall(
            id=f"R-{date.today().isoformat()}-{i}", for_date=date.today(),
            question=r.get("q",""), answer=r.get("a",""), project_id=r.get("project_id")
        ))
    db.commit()
    return resp

@router.post("/unstick", response_model=UnstickResponse)
def coach_unstick(
    req: UnstickRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    snippets = retrieve_snippets(user_id, f"Unstick: {req.context[:120]}", k=7)
    resp = call_llm_unstick(req, snippets)
    return resp

@router.get("/recall", response_model=RecallQuiz)
def coach_recall(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    items = db.query(Recall).filter(
        Recall.for_date <= date.today(),
        Recall.reviewed.is_(False)
    ).limit(5).all()

    payload = {
        "date": date.today().isoformat(),
        "items": [{"q": r.question, "a": r.answer} for r in items]
    }
    return RecallQuiz(**payload)
