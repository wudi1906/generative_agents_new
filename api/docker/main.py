from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from numpy import ndarray
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastembed.embedding import FlagEmbedding as Embedding

app = FastAPI()

# Initialize the model and tokenizer once rather than per request to save time and resources.
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
llm_model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")
embedding_model = Embedding(model_name="BAAI/bge-base-en", max_length=512) 

@app.get("/generate")
def generate(prompt: str):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = llm_model.generate(input_ids)
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return {"text": text}

class DocumentModel(BaseModel):
    documents: List[str]

@app.post("/embed")
def embed(document_model: DocumentModel):
    documents = document_model.documents
    embeddings: List[ndarray] = list(embedding_model.embed(documents))
    embeddings_json = [embedding.tolist() for embedding in embeddings]
    return {'embeddings': embeddings_json}