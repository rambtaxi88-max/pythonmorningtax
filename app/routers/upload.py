from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)

from fastapi.responses import Response

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserFile


router = APIRouter(
    prefix="/files",
    tags=["File Upload"]
)


# =========================================================
# UPLOAD FILE
# =========================================================

@router.post("/upload/{user_id}")
async def upload_file(
    user_id: int,
    file: UploadFile = File(...),
    content: str = Form(...),
    description: str = Form(...),
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

    # Read file
    file_bytes = await file.read()

    # Create file record
    db_file = UserFile(
        filename=file.filename or "unknown",
        content_type=file.content_type
        or "application/octet-stream",
        file_data=file_bytes,
        content=content,
        description=description,
        user_id=user_id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {
        "message": "File Uploaded Successfully",
        "file_id": db_file.id,
        "filename": db_file.filename,
        "content_type": db_file.content_type,
        "content": db_file.content,
        "description": db_file.description,
        "user_id": db_file.user_id
    }


# =========================================================
# GET ALL FILES
# =========================================================

@router.get("/")
def get_files(
    db: Session = Depends(get_db)
):

    files = db.query(UserFile).all()

    return {
        "message": "Files Retrieved Successfully",

        "data": [
            {
                "id": file.id,
                "filename": file.filename,
                "content_type": file.content_type,
                "content": file.content,
                "description": file.description,
                "user_id": file.user_id
            }
            for file in files
        ]
    }


# =========================================================
# GET FILE BY ID
# =========================================================

@router.get("/user/{user_id}")
def get_files_by_user_id(
    user_id: int,
    db: Session = Depends(get_db)
):

    # Check user exists
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    # Get only this user's files
    files = db.query(UserFile).filter(
        UserFile.user_id == user_id
    ).all()

    return {
        "message": "User Files Retrieved Successfully",
        "user_id": user_id,
        "total_files": len(files),

        "data": [
            {
                "id": file.id,
                "filename": file.filename,
                "content_type": file.content_type,
                "content": file.content,
                "description": file.description,
                "user_id": file.user_id
            }
            for file in files
        ]
    }
# =========================================================
# DOWNLOAD FILE BY ID
# =========================================================

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db)
):

    db_file = db.query(UserFile).filter(
        UserFile.id == file_id
    ).first()

    if not db_file:
        raise HTTPException(
            status_code=404,
            detail="File Not Found"
        )

    return Response(
        content=db_file.file_data,
        media_type=db_file.content_type,
        headers={
            "Content-Disposition":
            f'attachment; filename="{db_file.filename}"'
        }
    )


# =========================================================
# DELETE FILE
# =========================================================

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):

    db_file = db.query(UserFile).filter(
        UserFile.id == file_id
    ).first()

    if not db_file:
        raise HTTPException(
            status_code=404,
            detail="File Not Found"
        )

    db.delete(db_file)
    db.commit()

    return {
        "message": "File Deleted Successfully",
        "file_id": file_id
    }