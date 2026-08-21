from pydantic import BaseModel, EmailStr, ConfigDict


# =========================================================
# USER CREATE
# =========================================================

class UserCreate(BaseModel):

    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


# =========================================================
# USER LOGIN
# =========================================================

class UserLogin(BaseModel):

    username: str
    password: str


# =========================================================
# USER RESPONSE
# =========================================================

class UserResponse(BaseModel):

    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# FILE RESPONSE
# =========================================================

class FileResponse(BaseModel):

    id: int
    filename: str
    content_type: str
    content: str | None = None
    description: str | None = None
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# DEPENDENCY CREATE
# =========================================================

class DependencyCreate(BaseModel):

    father_name: str | None = None
    mother_name: str | None = None
    my_name: str | None = None
    wife_name: str | None = None
    child1: str | None = None
    child2: str | None = None
    child3: str | None = None


# =========================================================
# DEPENDENCY RESPONSE
# =========================================================

class DependencyResponse(BaseModel):

    id: int
    user_id: int

    father_name: str | None = None
    mother_name: str | None = None
    my_name: str | None = None
    wife_name: str | None = None

    child1: str | None = None
    child2: str | None = None
    child3: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )