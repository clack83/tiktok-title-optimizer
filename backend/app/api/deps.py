from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

# Re-export commonly used dependencies
CurrentUser = Depends(get_current_user)
SessionDep = Depends(get_db)
