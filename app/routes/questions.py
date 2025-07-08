from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from typing import List

router = APIRouter()

@router.post("/questions")
def create_question(q: schemas.QuestionCreate, db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    question = models.Question(**q.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@router.get("/questions", response_model=List[schemas.QuestionOut])
def get_all_questions(db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    return db.query(models.Question).all()

@router.get("/questions/{id}", response_model=schemas.QuestionOut)
def get_question(id: int, db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/questions/{id}")
def update_question(id: int, q: schemas.QuestionCreate, db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in q.dict().items():
        setattr(question, key, value)
    db.commit()
    return {"msg": "Question updated"}

@router.delete("/questions/{id}")
def delete_question(id: int, db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"msg": "Question deleted"}
