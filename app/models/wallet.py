from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Numeric(12,2),default=0)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    
    user=relationship("User", back_populates="wallet")
    sent_transaction = relationship("Transaction", foreign_keys="Transaction.sender_wallet_id", back_populates="sender_wallet")
    received_transaction = relationship("Transaction", foreign_keys="Transaction.receiver_wallet_id", back_populates="receiver_wallet")