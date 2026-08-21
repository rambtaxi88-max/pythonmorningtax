from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship


from database import Base


# =========================================================
# USER
# =========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    # User -> Files
    files = relationship(
        "UserFile",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # User -> Dependencies
    dependencies = relationship(
        "Dependency",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================================================
# USER FILE
# =========================================================

class UserFile(Base):

    __tablename__ = "user_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    content_type = Column(
        String(100),
        nullable=False
    )

    file_data = Column(
        LargeBinary,
        nullable=False
    )

    content = Column(
        String(500),
        nullable=True
    )

    description = Column(
        String(1000),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="files"
    )


# =========================================================
# DEPENDENCY
# =========================================================

class Dependency(Base):

    __tablename__ = "dependencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    father_name = Column(
        String(200),
        nullable=True
    )

    mother_name = Column(
        String(200),
        nullable=True
    )

    my_name = Column(
        String(200),
        nullable=True
    )

    wife_name = Column(
        String(200),
        nullable=True
    )

    child1 = Column(
        String(200),
        nullable=True
    )

    child2 = Column(
        String(200),
        nullable=True
    )

    child3 = Column(
        String(200),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="dependencies"
    )
