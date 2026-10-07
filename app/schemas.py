from pydantic import BaseModel, EmailStr, Field


class RecipientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class GenerationJobCreate(BaseModel):
    event_name: str = Field(..., min_length=2, max_length=200)
    certificate_title: str = Field(
        ...,
        min_length=2,
        max_length=200
    )
    recipients: list[RecipientCreate] = Field(
        ...,
        min_length=1
    )


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    file_path: str | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    id: int
    event_name: str
    certificate_title: str
    status: str
    total: int
    completed: int
    successful: int
    failed: int

    class Config:
        from_attributes = True