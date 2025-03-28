from rest_framework import generics
from drf_spectacular.utils import extend_schema

from .models import CVInstance
from .serializers import CVInstanceSerializer


class CVInstanceAPIView(generics.ListCreateAPIView):
    """List & Create CVs"""

    queryset = CVInstance.objects.all()
    serializer_class = CVInstanceSerializer

    @extend_schema(
        summary="List of CVs",
        description="Retrieves a list of CVs.",
        responses={200: CVInstanceSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new CV",
        description="Create a new CV instance with personal "
                    "information, skills, projects, and contacts.",
        request=CVInstanceSerializer,
        responses={201: CVInstanceSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CVInstanceDetailedAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Get, Update, Delete a CV"""
    queryset = CVInstance.objects.all()
    serializer_class = CVInstanceSerializer
