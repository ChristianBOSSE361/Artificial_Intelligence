#!../../../pytorch-env/bin/python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import *

app=FastAPI()
print("Application intancied properly")

app.add_middleware(
  CORSMiddleware, #usefull to allow to front end to have acces to the data  
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["POST", "GET"],
  allow_headers=["*"]
)

class ChatRequest(BaseModel):
    question: str #check if this is present and that it is a string
    conversation_id: str | None = None # same thing but either a string or nothing

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.question or req.question.strip() == "":
        raise HTTPException(status_code=400, detail="Empty question!!!")
    increase_computation_capacity()
    text_creation()
    chunks=chunks_creation()
    model,index=create_embeddings_and_store()

    result = text_generation(model, chunks, index,req.question, top_k=4)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}