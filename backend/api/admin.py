from django.contrib import admin

from . import models

@admin.register(models.PersonalLetter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'traits', 'output']