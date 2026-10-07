from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    certificate_id: int,
    recipient_name: str,
    event_name: str,
    certificate_title: str
) -> str:

    file_path = OUTPUT_DIR / f"certificate_{certificate_id}.pdf"

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=(page_width, page_height)
    )

    # Background
    pdf.setFillColor(colors.white)
    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # Outer border
    pdf.setStrokeColor(colors.HexColor("#1F4E79"))
    pdf.setLineWidth(5)

    pdf.rect(
        25,
        25,
        page_width - 50,
        page_height - 50,
        fill=0,
        stroke=1
    )

    # Certificate title
    pdf.setFillColor(colors.HexColor("#1F4E79"))
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 100,
        certificate_title
    )

    # Subtitle
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 145,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(colors.HexColor("#111111"))
    pdf.setFont("Helvetica-Bold", 30)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 205,
        recipient_name
    )

    # Description
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 15)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 255,
        f"For successfully participating in {event_name}"
    )

    # Event
    pdf.setFont("Helvetica-Bold", 17)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 290,
        event_name
    )

    # Footer
    pdf.setFont("Helvetica", 11)

    pdf.drawCentredString(
        page_width / 2,
        65,
        "Bulk Certificate Generator"
    )

    pdf.save()

    return str(file_path)