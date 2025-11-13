from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.deps import get_current_user
from schemas.user import UserUpdate

router = APIRouter(prefix="/api", tags=["user"])


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"email": user.email, "name": user.first_name}


@router.put("/me")
def update_me(data: UserUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(user, key, val)
    db.commit()
    return {"message": "Обновлено"}


@router.delete("/me")
def delete_me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    user.is_active = False
    db.commit()
    return {"message": "Удалён (мягко)"}
