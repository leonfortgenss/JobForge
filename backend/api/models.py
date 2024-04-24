from django.db import models

# Bara simpel modul där input är vad vi skrivit in och output är svar from ChatGPT

class PersonalLetter(models.Model):
    _input = models.TextField()
    _output = models.TextField()

    class Meta:
        db_table = "code_letter_creator"