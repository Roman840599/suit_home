from django.db import models


class Sensor(models.Model):
    datetime = models.DateTimeField(primary_key=True)
    temperature_value = models.CharField(max_length=20)

    def __str__(self):
        return self.title
