from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import User, Wallet, Transaction, FraudLog
from app.schemas.user import UserCreate
from app.schemas.transaction import TransactionCreate
from app.services.fraud import evaluate_transaction_fraud

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


@app.post("/transaction")
def create_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):
    sender_wallet = db.query(Wallet).filter(Wallet.id == txn.sender_wallet_id).first()
    receiver_wallet = (
        db.query(Wallet).filter(Wallet.id == txn.receiver_wallet_id).first()
    )

    if not sender_wallet or not receiver_wallet:
        return {"error": "Invalid wallet ID"}

    if sender_wallet.balance < txn.amount:
        transaction = Transaction(
            sender_wallet_id=txn.sender_wallet_id,
            receiver_wallet_id=txn.receiver_wallet_id,
            amount=txn.amount,
            status="BLOCKED",
        )
        db.add(transaction)
        db.commit()
        return {"message": "Insufficient balance. Transaction blocked."}

    risk_score, reasons = evaluate_transaction_fraud(
        db, sender_wallet_id=txn.sender_wallet_id, amount=txn.amount
    )

    if risk_score >= 50:
        transaction = Transaction(
            sender_wallet_id=txn.sender_wallet_id,
            receiver_wallet_id=txn.receiver_wallet_id,
            amount=txn.amount,
            status="BLOCKED",
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        fraud_log = FraudLog(
            transaction_id=transaction.id,
            risk_score=risk_score,
            reason=", ".join(reasons),
        )
        db.add(fraud_log)
        db.commit()

        return {
            "message": "Transaction blocked due to suspected fraud",
            "risk_score": risk_score,
            "reasons": reasons,
        }

    sender_wallet.balance -= txn.amount
    receiver_wallet.balance += txn.amount

    transaction = Transaction(
        sender_wallet_id=txn.sender_wallet_id,
        receiver_wallet_id=txn.receiver_wallet_id,
        amount=txn.amount,
        status="SUCCESS",
    )
    db.add(transaction)
    db.commit()
    return {"message": "Transaction successful", "transaction_id": transaction.id}
