from django.db import models


class CVInstance(models.Model):
    """
    CV Instance model
    main model of this task
    """

    firstname = models.CharField(null=True, blank=True, max_length=60)
    lastname = models.CharField(null=True, blank=True, max_length=60)
    skills = models.JSONField()
    projects = models.JSONField()
    bio = models.TextField()
    contacts = models.JSONField()
