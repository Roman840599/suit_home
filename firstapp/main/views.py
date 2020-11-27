from django.shortcuts import render
from .models import Sensor


def index(request):
    sensors = Sensor.objects.order_by('-id')[:1]
    return render(request, 'main/index.html', {'sensors': sensors})
