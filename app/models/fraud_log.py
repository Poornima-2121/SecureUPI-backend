from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class FraudLog(Base):
    __tablename__ = "fraud_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    risk_score = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    flagged_at = Column(DateTime(timezone=True),server_default=func.now())