from django.contrib import admin
from . import models


class CVInstanceAdmin(admin.ModelAdmin):
    """
    CV Instance admin class
    """
    list_display = (
        'id', 'firstname', 'lastname', 'skills',
        'bio', 'projects', 'contacts',
    )
    list_filter = ('firstname', 'lastname',)


class RequestLogAdmin(admin.ModelAdmin):
    """
    Request LogA admin class
    """
    list_display = (
        'id', 'http_method', 'path', 'timestamp',
    )
    list_filter = ('http_method', 'timestamp',)


admin.site.register(models.CVInstance, CVInstanceAdmin)
admin.site.register(models.RequestLog, RequestLogAdmin)
