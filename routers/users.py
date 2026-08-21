from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext



import crud
import models
import schemas
from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=schemas.UserResponse
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_username = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    return crud.create_user(db, user)


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()


    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Username"
        )


    if not pwd_context.verify(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )


    return {
        "message": "Login Successful",
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }


# =========================================================
# GET ALL USERS
# =========================================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(models.User).all()

    return {
        "message": "Users Retrieved Successfully",
        "data": users
    }


# =========================================================
# GET USER BY ID
# =========================================================

@router.get("/users/{id}")
def get_user(
    id: int,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.id == id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )


    return user


# =========================================================
# UPDATE USER
# =========================================================

@router.put("/users/{id}")
def update_user(
    id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.id == id
    ).first()


    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )


    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email


    db.commit()
    db.refresh(db_user)


    return {
        "message": "User Updated Successfully",
        "data": db_user
    }


# =========================================================
# DELETE USER
# =========================================================

@router.delete("/users/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.id == id
    ).first()


    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )


    db.delete(db_user)
    db.commit()


    return {
        "message": "User Deleted Successfully"
    }
