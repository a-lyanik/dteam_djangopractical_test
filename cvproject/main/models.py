from django.db import models
from django.core.exceptions import ValidationError


def validate_list_of_strings(value):
    """Ensure the value is a list of non-empty strings."""
    if not isinstance(value, list):
        raise ValidationError("Must be a list.")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValidationError("Each item must be a non-empty string.")


def validate_dict_of_strings(value):
    """Ensure the value is a dictionary with string keys and values."""
    if not isinstance(value, dict):
        raise ValidationError("Must be a dictionary.")
    if any(not isinstance(k, str)
           or not isinstance(v, str) for k, v in value.items()):
        raise ValidationError(
            "All keys and values must be non-empty strings.")


class CVInstance(models.Model):
    """
    CV Instance model
    main model of this task
    """

    firstname = models.CharField(null=True, blank=True, max_length=60)
    lastname = models.CharField(null=True, blank=True, max_length=60)
    skills = models.JSONField(validators=[validate_list_of_strings])
    projects = models.JSONField(validators=[validate_list_of_strings])
    bio = models.TextField()
    contacts = models.JSONField(validators=[validate_dict_of_strings])


class RequestLog(models.Model):
    http_method = models.CharField(null=False, blank=False, max_length=10)
    path = models.CharField(null=False, blank=False, max_length=260)
    timestamp = models.DateTimeField(auto_now_add=True)
