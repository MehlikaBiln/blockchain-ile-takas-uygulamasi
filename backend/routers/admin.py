from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Transaction
from auth import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])


# Admin kullanıcılarını listele
@router.get("/admin/users")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yönetici yetkisi gereklidir.")

    users = db.query(User).all()
    return users


@router.get("/admin/transactions")
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yönetici yetkisi gereklidir.")

    transactions = db.query(Transaction).all()
    return transactions


@router.put("/admin/update-role")
def update_user_role(user_email: str, new_role: str, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yönetici yetkisi gereklidir.")

    # Yeni rol sadece 'admin' veya 'user' olabilir
    if new_role not in ['admin', 'user']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Geçersiz rol.")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı.")

    user.role = new_role
    db.commit()
    return {"message": f"Kullanıcı rolü başarıyla {new_role} olarak güncellendi."}
