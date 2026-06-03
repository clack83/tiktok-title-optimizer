from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.preference import UserPreference
from app.schemas.preference import PreferenceUpdate, PreferenceResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/preferences", response_model=PreferenceResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        return PreferenceResponse(
            user_id=str(current_user.id),
            preferences={"default_strategy": "auto", "max_title_length": 80, "category": None},
        )
    return PreferenceResponse(user_id=str(pref.user_id), preferences=pref.preferences)


@router.put("/preferences", response_model=PreferenceResponse)
def update_preferences(
    req: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id, preferences={})
        db.add(pref)

    pref.preferences = req.model_dump(exclude_none=True)
    db.commit()
    db.refresh(pref)
    return PreferenceResponse(user_id=str(pref.user_id), preferences=pref.preferences)
