from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.access import AccessRule
from auth.deps import get_current_user

router = APIRouter(prefix="/api/admin", tags=["admin"])


def require_admin(user=Depends(get_current_user)):
    if "admin" not in [r.name for r in user.roles]:
        raise HTTPException(403)
    return user


@router.get("/rules")
def get_rules(user=Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(AccessRule).all()


@router.post("/rules")
def create_rule(data: dict, user=Depends(require_admin), db: Session = Depends(get_db)):
    rule = AccessRule(**data)
    db.add(rule)
    db.commit()
    return {"message": "Создано"}
