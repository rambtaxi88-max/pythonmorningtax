from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db
from models import User, Dependency
from schemas import (
    DependencyCreate,
    DependencyResponse
)


router = APIRouter(
    prefix="/dependency",
    tags=["Dependency"]
)


# =========================================================
# CREATE DEPENDENCY
# =========================================================

@router.post(
    "/{user_id}",
    response_model=DependencyResponse
)
def create_dependency(
    user_id: int,
    dependency: DependencyCreate,
    db: Session = Depends(get_db)
):

    # Check user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    # Create dependency
    db_dependency = Dependency(

        father_name=dependency.father_name,

        mother_name=dependency.mother_name,

        my_name=dependency.my_name,

        wife_name=dependency.wife_name,

        child1=dependency.child1,

        child2=dependency.child2,

        child3=dependency.child3,

        user_id=user_id
    )

    db.add(
        db_dependency
    )

    db.commit()

    db.refresh(
        db_dependency
    )

    return db_dependency


# =========================================================
# GET ALL DEPENDENCIES
# =========================================================

@router.get("/")
def get_dependencies(
    db: Session = Depends(get_db)
):

    dependencies = db.query(
        Dependency
    ).all()

    return {
        "message": "Dependencies Retrieved Successfully",
        "data": dependencies
    }


# =========================================================
# GET DEPENDENCY BY ID
# =========================================================

@router.get("/{dependency_id}")
def get_dependency(
    dependency_id: int,
    db: Session = Depends(get_db)
):

    dependency = db.query(
        Dependency
    ).filter(
        Dependency.id == dependency_id
    ).first()

    if not dependency:

        raise HTTPException(
            status_code=404,
            detail="Dependency Not Found"
        )

    return dependency


# =========================================================
# DELETE DEPENDENCY
# =========================================================

@router.delete("/{dependency_id}")
def delete_dependency(
    dependency_id: int,
    db: Session = Depends(get_db)
):

    dependency = db.query(
        Dependency
    ).filter(
        Dependency.id == dependency_id
    ).first()

    if not dependency:

        raise HTTPException(
            status_code=404,
            detail="Dependency Not Found"
        )

    db.delete(
        dependency
    )

    db.commit()

    return {
        "message": "Dependency Deleted Successfully"
    }
