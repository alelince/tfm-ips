from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, security
from ..database import get_db

router = APIRouter()

@router.post("/login", status_code=200)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid username")
    if not security.verify_password(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    access_token = security.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(security.oauth2_scheme),
                           db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="invalid credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload: dict = security.decode_access_token(token)
        username: str = payload.get("sub", None)
        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
