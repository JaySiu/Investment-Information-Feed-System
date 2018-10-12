from django.db import models
from main import main

class TA(models.Model):
    bbands = models.ImageField()

    #def __init__(self):
    #    self.bbands =
