# Bulk Certificate Generator

A backend API for generating certificates in bulk for event or course participants.

The system accepts a list of recipients, validates their information, creates a generation job, generates individual PDF certificates in the background, tracks progress, handles individual failures, and allows generated certificates to be downloaded.

## Technology Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- ReportLab
- Pytest
- Uvicorn

## Features

- Bulk certificate generation
- Input validation
- Background processing
- Job status tracking
- Success and failure tracking
- Individual PDF certificate generation
- Certificate download
- Automated tests
- Swagger API documentation

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── routes/
│   │   ├── jobs.py
│   │   └── certificates.py
│   │
│   └── services/
│       └── certificate_generator.py
│
├── generated_certificates/
├── templates/
├── tests/
├── database.db
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Create a generation job

```http
POST /jobs
```

Example request:

```json
{
  "event_name": "Python Workshop 2026",
  "certificate_title": "Certificate of Participation",
  "recipients": [
    {
      "name": "Ashirwad Jadhav",
      "email": "ashirwad@example.com"
    },
    {
      "name": "Rahul Kumar",
      "email": "rahul@example.com"
    }
  ]
}
```

Example response:

```json
{
  "job_id": 1,
  "status": "queued",
  "total": 2
}
```

The API returns the job ID immediately while certificates are generated in the background.

### Check job status

```http
GET /jobs/{job_id}
```

Example:

```http
GET /jobs/1
```

Example response:

```json
{
  "job_id": 1,
  "event_name": "Python Workshop 2026",
  "certificate_title": "Certificate of Participation",
  "status": "completed",
  "total": 2,
  "completed": 2,
  "successful": 2,
  "failed": 0
}
```

### Retrieve a certificate

```http
GET /certificates/{certificate_id}
```

Example:

```http
GET /certificates/1
```

The generated PDF is returned by the API.

## Validation

The API validates:

- Recipient name
- Recipient email
- Event name
- Certificate title
- At least one recipient

Invalid input returns HTTP `422`.

Example invalid email:

```json
{
  "name": "Test User",
  "email": "invalid-email"
}
```

## Failure Handling

Each recipient is processed independently.

For example:

```text
Recipient 1 → SUCCESS
Recipient 2 → SUCCESS
Recipient 3 → FAILED
Recipient 4 → SUCCESS
```

If one certificate fails, the remaining certificates continue to be generated.

The failed certificate stores the error message in the database.

## Bulk Processing

The application uses FastAPI background tasks.

The client does not have to wait for every PDF to be generated.

The process is:

```text
Client
   │
   ▼
POST /jobs
   │
   ▼
Create Job
   │
   ▼
Return job_id
   │
   ▼
Background processing
   │
   ├── Generate Certificate
   ├── Generate Certificate
   ├── Generate Certificate
   └── ...
   │
   ▼
Update job progress
```

For a production system with extremely large workloads, a dedicated task queue such as Celery with Redis could be introduced.

## Database Design

The application uses SQLite as the relational database and SQLAlchemy as the ORM.

### Jobs table

Stores:

- Job ID
- Event name
- Certificate title
- Status
- Total recipients
- Completed count
- Successful count
- Failed count

### Certificates table

Stores:

- Certificate ID
- Job ID
- Recipient name
- Recipient email
- Status
- Generated PDF path
- Error message

Relationship:

```text
One Job
   │
   ├── Certificate
   ├── Certificate
   ├── Certificate
   └── Certificate
```

## Certificate Generation

Certificates are generated as PDF files using ReportLab.

Generated files are stored in:

```text
generated_certificates/
```

Example:

```text
certificate_1.pdf
certificate_2.pdf
certificate_3.pdf
```

## Testing

Run all tests using:

```powershell
pytest -v
```

The tests cover:

- Creating a generation job
- Input validation
- Certificate generation
- Job status/progress
- Individual certificate failure
- Certificate retrieval

## Design Decisions

### FastAPI

FastAPI provides automatic request validation, OpenAPI documentation, dependency injection, and easy testing.

### SQLite

SQLite satisfies the relational database requirement without requiring a separate database server.

The application can later be migrated to PostgreSQL using SQLAlchemy.

### SQLAlchemy

SQLAlchemy separates database operations from the API logic and provides an ORM-based approach.

### ReportLab