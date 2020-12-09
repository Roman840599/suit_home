from class_creator import MyMQTTClass
import time
import random
import os

pid = os.getpid()
thermometer = MyMQTTClass(pid)

while True:
    temperature = random.randrange(10, 30, 1)
    host = '127.0.0.1'
    topic = 'sensor/thermometer/' + str(pid) + '/temperature'
    currentQoS = 0
    thermometer.push_message(host, topic, currentQoS, temperature)
    time.sleep(5)




