from pydantic import BaseModel, Field
from decimal import Decimal

class TransactionCreate(BaseModel):
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: Decimal = Field(gt=0)