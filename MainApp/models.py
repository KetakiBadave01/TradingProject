from django.db import models
from django.db import models
# Create your models here.
class Candle(models.Model):
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField()
