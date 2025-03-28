from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from weasyprint import HTML

from .models import CVInstance


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
