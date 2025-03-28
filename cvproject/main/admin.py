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


admin.site.register(models.CVInstance, CVInstanceAdmin)
