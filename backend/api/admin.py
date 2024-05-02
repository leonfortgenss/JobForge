from django.contrib import admin

from . import models

@admin.register(models.PersonalLetter)
class CarAdmin(admin.ModelAdmin):
    list_display = ['_input', "_output"]