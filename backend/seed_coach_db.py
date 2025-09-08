# backend/seed_coach_db.py
import uuid
from datetime import date
from backend.database import SessionLocal
from backend.models_coach import Project, Task, Base, engine

def seed_data():
    """Seeds the database with one demo project and three demo tasks."""
    db = SessionLocal()

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    try:
        # Check if project already exists
        existing_project = db.query(Project).filter_by(id="P1").first()
        if existing_project:
            print("Demo data already exists. Skipping seed.")
            return

        print("Seeding database with demo data...")

        # 1. Create a Demo Project
        demo_project = Project(
            id="P1",
            name="AURA Coach MVP",
            status="active",
            milestone="Finish backend routes",
            priority=5
        )
        db.add(demo_project)

        # 2. Create Demo Tasks
        tasks = [
            Task(
                id=f"T{i+1}",
                project_id="P1",
                title=title,
                status="todo",
                priority=5-i,
                due_date=date(2025, 8, 22),
                est_minutes=25
            ) for i, title in enumerate([
                "Implement login POST endpoint",
                "Write happy-path test for login",
                "Wire up frontend login button"
            ])
        ]
        db.add_all(tasks)
        
        db.commit()
        print("Successfully seeded database.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
