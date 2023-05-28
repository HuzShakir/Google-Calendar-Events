from django.db import models

class Calender(models.Model):
    event = models.CharField(max_length = 180)

