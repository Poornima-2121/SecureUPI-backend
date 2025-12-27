from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status":"OK"}