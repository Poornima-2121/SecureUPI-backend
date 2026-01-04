from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import User, Wallet, Transaction, FraudLog
from app.schemas.user import UserCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password,  # to be hashed later
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    wallet = Wallet(user_id=new_user.id, balance=0)
    db.add(wallet)
    db.commit()

    return {"message": "User and wallet created successfully", "user_id": new_user.id}
