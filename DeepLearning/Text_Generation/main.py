#!../../../pytorch-env/bin/python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import *

app=FastAPI()
print("Application intancied properly")

app.add_middleware(
  CORSMiddleware, #usefull to allow to front end to have acces to the data  
  allow_origins=["http://localhost:5173/"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str #check if this is present and that it is a string
    conversation_id: str | None = None # same thing but either a string or nothing

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.question or req.question.strip() == "":
        raise HTTPException(status_code=400, detail="Empty question!!!")
    increase_computation_capacity()
    return text_generation(req.question, top_k=4)
    
##the current problem is to know how the front send a message to the back , his format and so one.
@app.get("/health")
def health():
    return {"status": "ok"}