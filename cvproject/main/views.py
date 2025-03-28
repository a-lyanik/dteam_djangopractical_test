from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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
