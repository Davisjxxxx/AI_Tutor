# schemas_coach.py
from pydantic import BaseModel, Field, conint
from typing import List, Optional, Literal

class AMTopTask(BaseModel):
    task_id: str
    title: str
    minutes: conint(gt=0, le=30) = 25
    test: Optional[str] = None

class AMTimebox(BaseModel):
    task_id: str
    start_suggestion: str  # "09:15"
    minutes: conint(gt=0, le=60)

class AMStudySlot(BaseModel):
    topic: str
    plan: str
    minutes: conint(gt=5, le=30) = 15

class AMResponse(BaseModel):
    focus_project: dict
    top3_today: List[AMTopTask]
    timebox_plan: List[AMTimebox]
    study_slot: AMStudySlot
    risk: str

class PMShipped(BaseModel):
    title: str

class PMBlocker(BaseModel):
    description: str
    next_step: str

class PMResponse(BaseModel):
    shipped: List[PMShipped]
    learned: List[str]  # 3 bullets
    blockers: List[PMBlocker]
    tomorrow_top3: List[AMTopTask]
    create_recalls: List[dict]  # {q, a, project_id?}
    coach_note: str

class UnstickRequest(BaseModel):
    project_id: str
    context: str  # REPRO + ERROR + snippet

class UnstickResponse(BaseModel):
    hypotheses: List[str]
    minimal_repro: str
    smallest_change: str
    rollback_plan: str

class RecallQA(BaseModel):
    q: str
    a: str

class RecallQuiz(BaseModel):
    date: str
    items: List[RecallQA]
