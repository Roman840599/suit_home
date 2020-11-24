from class_creator import MyMQTTClass
import time
import sys
import os

pid = os.getpid()
thermometer = MyMQTTClass(pid)

while True:
    thermometer.push_message('127.0.0.1', 'thermometer/' + str(pid) + '/temperature', 0)
    time.sleep(5)




