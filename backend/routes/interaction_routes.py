from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/interactions")
def create(data: schemas.InteractionCreate, db: Session = Depends(get_db)):
    obj = models.Interaction(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/interactions")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Interaction).all()

@router.delete("/interactions/{id}")
def delete_interaction(id: int, db: Session = Depends(get_db)):
    interaction = db.query(models.Interaction).filter(models.Interaction.id == id).first()

    if not interaction:
        return {"error": "Interaction not found"}

    db.delete(interaction)
    db.commit()

    return {"message": "Interaction deleted successfully"}