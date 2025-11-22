#!../../../pytorch-env/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
  CORSMiddleware, #usefull to allow to front end to have acces to the data  
  allow_origins=["http://localhost:5173/"],
  allow_credentials=True,
  allow_methods=["POST", "GET"],
  allow_headers=["*"]
)

class Question(BaseModel):
    question: str

@app.post("/chat")
async def chat(q: Question):
    return {"answer": f"Vous avez dit : {q.question}", "sources": []}