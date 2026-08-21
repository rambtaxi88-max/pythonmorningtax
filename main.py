from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



from database import Base, engine
import models
from routers import users
from routers import upload
from routers import dependency

# IMPORTANT:
# This imports User, UserFile and Dependency
# so SQLAlchemy registers them in Base.metadata.





# Create all SQLAlchemy tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MorningTax API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://187.52.119.33:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(upload.router)
app.include_router(dependency.router)
