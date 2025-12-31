from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Wallet, Transaction, FraudLog

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status":"OK"}