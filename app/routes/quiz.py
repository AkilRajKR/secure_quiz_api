import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from typing import List

router = APIRouter()

@router.get("/quiz", response_model=List[schemas.QuestionOut])
def get_quiz_questions(db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    questions = db.query(models.Question).all()
    if len(questions) < 2:
        raise HTTPException(status_code=400, detail="Not enough questions in the database")
    selected = random.sample(questions, 2)
    return selected

@router.post("/quiz/result")
def submit_quiz(submission: schemas.QuizSubmission, db: Session = Depends(utils.get_db), user=Depends(utils.get_current_user)):
    score = 0
    total = len(submission.answers)
    correct_answers = {}
    for qid, answer in submission.answers.items():
        question = db.query(models.Question).filter(models.Question.id == qid).first()
        if question:
            correct_answers[qid] = question.correct_option
            if answer == question.correct_option:
                score += 1
    result = models.Result(user_id=user.id, score=score, total=total)
    db.add(result)
    db.commit()
    return {
        "score": score,
        "total": total,
        "correct_answers": correct_answers
    }
