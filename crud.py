from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_user(db: Session, user):

    hashed_password = pwd_context.hash(
        user.password
    )

    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user