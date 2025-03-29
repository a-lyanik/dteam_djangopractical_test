import os
import base64
import requests

from weasyprint import HTML
from celery import shared_task

from django.template.loader import render_to_string
from django.conf import settings

from .models import CVInstance


@shared_task
def send_cv_email(cv_id, email):

    cv = CVInstance.objects.get(pk=cv_id)

    # Render HTML to PDF
    html_string = render_to_string(
        "main/cvinstance_detail.html",
        {"object": cv, "pdf_mode": True})
    pdf_file = HTML(string=html_string).write_pdf()
    encoded_pdf = base64.b64encode(pdf_file).decode()

    # Define the API URL and headers
    headers = {
        'Authorization': f'Bearer {settings.MAILTRAP_KEY}',
        'Content-Type': 'application/json'
    }

    # Define the email data payload
    data = {
        "from": {
            "email": "hello@demomailtrap.co",
            "name": "Mailtrap Test"
        },
        "to": [
            {"email": email}
        ],
        "subject": f"CV of {cv.firstname} {cv.lastname}",
        "text": f"Attached is the CV of {cv.firstname} {cv.lastname}.",
        "category": "Integration Test",
        "attachments": [
            {
                "filename": f"{cv.firstname}_{cv.lastname}_CV.pdf",
                "content": encoded_pdf,
                "type": "application/pdf"
            }
        ]
    }

    response = requests.post(
        settings.MAILTRAP_URL, headers=headers, json=data)

    return response.status_code, response.json()
