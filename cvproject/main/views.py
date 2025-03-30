import json
from django.http import HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template

from weasyprint import HTML

from .models import CVInstance, RequestLog
from .tasks import send_cv_email
from .utils import translate_text


class CVInstanceDetailView(DetailView):
    """
    CVInstance detail view
    """
    model = CVInstance
    context_object_name = 'cv_instances'


class CVInstanceListView(ListView):
    """
    CVInstance list view
    """
    model = CVInstance
    context_object_name = 'cv_instances'


def generate_cv_pdf(request, pk):
    """
    Generate a CV pdf file
    """
    cv = get_object_or_404(CVInstance, id=pk)
    # Use the existing template
    template = get_template("main/cvinstance_detail.html")
    html_content = template.render(
        {"object": cv, "pdf_mode": True})  # Pass a flag for styling

    # Generate the PDF
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = \
        f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'

    return response


def request_log_list(request):
    """View to display the last 10 logged requests."""
    logs = RequestLog.objects.values(
        "http_method", "path", "timestamp").order_by("-timestamp")[:10]
    return render(
        request,
        "main/request_log_list.html",
        {"logs": logs}
    )


def settings_view(request):
    """
    View to display selected Django settings using the context processor.
    """
    return render(request, "main/settings.html")


def send_cv_email_view(request, pk):
    """
    View to send a CV pdf email
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            if not email:
                return JsonResponse({"message": "Invalid email"}, status=400)

            send_cv_email.delay(pk, email)  # Call Celery task
            return JsonResponse({"message": "Email is being sent."})
        except Exception as e:
            return JsonResponse({"message": "Error occurred"}, status=500)


def translate_cv(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        target_language = data.get("language")
        translated_text = translate_text(pk, target_language)
        return JsonResponse({"translated_text": translated_text})
    return JsonResponse({"error": "Invalid request"}, status=400)
