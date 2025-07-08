from fastapi import FastAPI
from .database import Base, engine
from .routes import users, questions, quiz


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)
app.include_router(questions.router)
app.include_router(quiz.router)
