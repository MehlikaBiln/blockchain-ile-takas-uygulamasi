from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
import models
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import User

# JWT ayarları
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()
security = HTTPBearer()  # ✅ Değiştirildi

# Kullanıcı kayıt
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    city: str
    neighborhood: str

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")

    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        city=user.city,
        neighborhood=user.neighborhood
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kullanıcı başarıyla kaydedildi."}

# Kullanıcı giriş
class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if not user_in_db or not pwd_context.verify(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre.")

    token_data = {"sub": user_in_db.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Kullanıcı kimliğini doğrula (HTTPBearer ile)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulama başarısız.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me")
def read_profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role,
        "name": current_user.name
    }


def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlemi yapmak için admin olmanız gerekiyor."
        )
    return current_user

