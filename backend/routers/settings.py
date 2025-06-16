from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import get_admin_user
from database import get_db
from models import Settings, User
from pydantic import BaseModel

router = APIRouter(prefix="/settings", tags=["Settings"])



class SettingsUpdate(BaseModel):
    only_same_neighborhood: bool

@router.put("/settings/update")
def update_settings(
    settings_data: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings(only_same_neighborhood=settings_data.only_same_neighborhood)
        db.add(settings)
    else:
        settings.only_same_neighborhood = settings_data.only_same_neighborhood
    db.commit()
    return {"message": "Ayar başarıyla güncellendi.", "only_same_neighborhood": settings.only_same_neighborhood}


