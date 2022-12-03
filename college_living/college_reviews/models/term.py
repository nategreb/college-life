from django.db import models


class Term(models.Model):
    term_year = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=11)