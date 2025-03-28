from rest_framework import serializers
from .models import CVInstance


class CVInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVInstance
        fields = '__all__'  # Include all fields
