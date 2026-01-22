from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from app.models import Transaction, FraudLog, Wallet

HIGH_AMOUNT_THRESHOLD = Decimal("5000")
RISK_THRESHOLD = 50


def evaluate_transaction_fraud(db: Session, sender_wallet_id: int, amount: Decimal):
    risk_score = 0
    reasons = []

    # Rule 1: High amount
    if amount > HIGH_AMOUNT_THRESHOLD:
        risk_score += 50
        reasons.append("High transaction amount")

    # Rule 2: Rapid transaction (last 1 minute)
    one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

    recent_txn_count = (
        db.query(func.count(Transaction.id))
        .filter(
            Transaction.sender_wallet_id == sender_wallet_id,
            Transaction.created_at >= one_minute_ago,
            Transaction.status == "SUCCESS",
        )
        .scalar()
    )

    if recent_txn_count >= 3:
        risk_score += 50
        reasons.append("Too many transactions in short time")

    return risk_score, reasons
