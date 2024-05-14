from django.db import models

# Bara simpel modul där input är vad vi skrivit in och output är svar from ChatGPT

class PersonalLetter(models.Model):
    name = models.TextField()
    age = models.TextField()
    traits = models.TextField()
    # Väntar med dessa sålänge tills vi vet hur datan ser ut
    # company = models.TextField()
    # company_description = models.TextField()
    output = models.TextField()

    class Meta:
        db_table = "letter_creator"