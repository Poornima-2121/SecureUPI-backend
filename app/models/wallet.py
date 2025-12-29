from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy import func
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Numeric(12,2),default=0)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())