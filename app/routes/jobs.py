from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, Certificate
from app.schemas import GenerationJobCreate
from app.services.certificate_generator import generate_certificate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


def process_job(job_id: int):
    from app.database import SessionLocal

    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        certificates = (
            db.query(Certificate)
            .filter(Certificate.job_id == job_id)
            .all()
        )

        for certificate in certificates:

            try:
                file_path = generate_certificate(
                    certificate_id=certificate.id,
                    recipient_name=certificate.recipient_name,
                    event_name=job.event_name,
                    certificate_title=job.certificate_title
                )

                certificate.status = "success"
                certificate.file_path = file_path

                job.successful += 1

            except Exception as error:

                certificate.status = "failed"
                certificate.error_message = str(error)

                job.failed += 1

            finally:
                job.completed += 1
                db.commit()

        job.status = "completed"
        db.commit()

    except Exception:
        job.status = "failed"
        db.commit()

    finally:
        db.close()


@router.post("")
def create_generation_job(
    request: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    job = Job(
        event_name=request.event_name,
        certificate_title=request.certificate_title,
        status="queued",
        total=len(request.recipients),
        completed=0,
        successful=0,
        failed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="pending"
        )

        db.add(certificate)

    db.commit()

    background_tasks.add_task(
        process_job,
        job.id
    )

    return {
        "job_id": job.id,
        "status": "queued",
        "total": job.total
    }

@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "certificate_title": job.certificate_title,
        "status": job.status,
        "total": job.total,
        "completed": job.completed,
        "successful": job.successful,
        "failed": job.failed
    }