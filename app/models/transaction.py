from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    receiver_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    status = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sender_wallet = relationship("Wallet", foreign_keys=[sender_wallet_id], back_populates="sent_transactions")
    receiver_wallet = relationship("Wallet", foreign_keys=[receiver_wallet_id], back_populates="received_transactions")
    fraud_log = relationship("FraudLog", back_populates="transaction", uselist=False)