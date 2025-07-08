from pydantic import BaseModel, EmailStr
from typing import Dict, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    accessToken: str

class QuestionCreate(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

class QuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        orm_mode = True

class QuizSubmission(BaseModel):
    answers: Dict[int, str]  
