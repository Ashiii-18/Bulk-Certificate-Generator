from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routes.jobs import router as jobs_router
from app.routes.certificates import router as certificates_router

app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for bulk certificate generation",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(jobs_router)
app.include_router(certificates_router)


@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running"
    }