from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models import Transaction, User
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/transactions/history")
def get_transaction_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(
        (Transaction.sender == current_user.email) | (Transaction.receiver == current_user.email)
    ).order_by(Transaction.timestamp.desc()).all()

    return {
        "user": current_user.email,
        "history": [
            {
                "id": t.id,
                "sender": t.sender,
                "receiver": t.receiver,
                "item": t.item,
                "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M")
            }
            for t in transactions
        ]
    }
