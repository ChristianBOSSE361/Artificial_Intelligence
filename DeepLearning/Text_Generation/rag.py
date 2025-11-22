#!../../../pytorch-env/bin/python
#Because we work in an environment

"""
This code contain everything contained in the notebook file and nothing more.
Things are just adjust to make it simple for building an interface

author: Christian BOSSE
date: Monday Nov. 10 2025
"""

import torch
import pdfplumber
import os
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv #because I work in a virtual environement


def increase_computation_capacity():
    """
    Just to make our computation faster in case we do not have GPU card
    """
    if torch.cuda.is_available():
        print("GPU is available.")
        device = torch.cuda.current_device()
    else:
        print("Will work on CPU.")
        print(torch.get_num_threads())
        torch.set_num_threads(8)
        print("Cores used now:", torch.get_num_threads())



def text_creation(pdf_name="../data/Machine Learning For Absolute Beginners_ A Plain English Introduction (Second Edition) - Machine Learning For Absolute Beginners.pdf"):
    #Download
    with pdfplumber.open(pdf_name) as pdf:
        completed_text=""
        for page in pdf.pages:
            completed_text+=page.extract_text()+"\n"

    # We put it into a text file
    text_name="/home/christian/ProjetsPerso/Artificial_Intelligence/DeepLearning/Text_Generation/data/text.txt"
    if os.path.exists(text_name): os.remove(text_name)

    with open(text_name, "w", encoding="utf-8") as text:
        text.write(completed_text)



def chunks_creation(text_name,display=False):
    """
    The goal of this function is to clean the data(the text) and to create the chunks
    """
    texts=""
    with open(text_name, 'r', encoding="utf-8") as f:
        texts=f.read()

    # Cleaning part
    ##Every word, pontuation, symbole could be important for the understanding of the text
    ##So we decide to keep everything and to only delete successive space and emails.
    print("Size before cleaning:", len(texts.split()))
    texts=re.sub(pattern=r'\S+@\S+', repl=' ', string=texts)
    texts=re.sub(pattern=r'\s+', repl=' ', string=texts) # notice that here the order is important :)

    # Made it into chunks
    texts=texts.split()
    print("Size after cleaning:", len(texts))
    CHUNK_SIZE=200

    chunks=[" ".join(texts[i:i+CHUNK_SIZE]) for i in range(0,len(texts),CHUNK_SIZE)]

    #Just a little display
    if display:
        print("===Display====")
        for i in range(3):
            print(f"\tChunk {i} :", chunks[i])
        print("Number of chunks:", len(chunks))
    
    return chunks


def create_embeddings_and_store(chunks):
    """
    This function create the embeddings using the chunks and store them using faiss index
    """

    model=SentenceTransformer("all-MiniLM-L6-v2")
    #print(model)
    embeddings=[model.encode(chunk) for chunk in chunks]
    embeddings=np.array(embeddings, dtype="float32")
    print(f"Embeddings created whith shape of {embeddings.shape}.")

    #Creation of the index
    dim=embeddings.shape[1] 
    index=faiss.IndexFlatIP(dim) #we pass dim as a parameter cause this function need to know the dimension of the vectors for allocating memory for storing
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True) #normalization for the cosinus similarity
    index.add(embeddings) #we add our data to that index

    #storing
    faiss.write_index(index, "./data/index.faiss")

    # storing the chunks to retrieve the text later but not usefull now
    # with open("chunks.json", "w", encoding="utf-8") as f:
    #     json.dump(chunks, f, ensure_ascii=False, indent=2)
    return model, index


def text_generation(query="What is Machine learning?", top_k=3):
    """
    We generate the anwswers using a GPT.
    """
    # we search first the data
    model=SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("./data/index.faiss")
    with open("./data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    #Get the query
    query_embedding=model.encode(query)
    query_embedding=np.array([query_embedding], dtype='float32')
    query_embedding=query_embedding/np.linalg.norm(query_embedding, axis=1, keepdims=True)

    #Gather all the good chunks
    D,I=index.search(query_embedding,k=top_k) #Here D correspond to a matrix of distance and I a matrix of index
    context = "\n\n".join(chunks[i] for i in I[0])

    prompt=f"""
    Focusing on the following passages, build an anwser.

    Text to focus on:{context}

    Question:{query}
    Answer(simple, not too long, precise and with examples if possible):
    """
    ##generate the answer
    #loading environment variable
    load_dotenv()

    client = InferenceClient(
        api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    )

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-1B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    #print(completion.choices[0].message.content)

    return completion.choices[0].message.content