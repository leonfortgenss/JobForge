from django.db import models
from django.contrib.auth.models import User

# Bara simpel modul där input är vad vi skrivit in och output är svar from ChatGPT

class PersonalLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.TextField()
    age = models.TextField()
    traits = models.TextField()
    programming_language = models.TextField(default="")
    employer_link = models.TextField(default="")
    skill_match = models.JSONField(null=True, blank=True)
    output = models.TextField()

    class Meta:
        db_table = "letter_creator"