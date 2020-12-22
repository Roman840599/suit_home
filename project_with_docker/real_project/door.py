from class_creator import MyMQTTClass
import time
import random
import os

pid = os.getpid()
door = MyMQTTClass(pid)

while True:
    door_status = random.choice(['open', 'closed'])
    host = '127.0.0.1'
    port = 1883
    topic = 'sensor/door/' + str(pid) + '/status'
    currentQoS = 2
    door.push_message(host, port, topic, currentQoS, door_status)
    time.sleep(5)