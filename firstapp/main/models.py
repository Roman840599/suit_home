from django.db import models


class Sensor(models.Model):
    title = models.CharField('average_temperature', max_length=20)

    def __str__(self):
        return self.title
