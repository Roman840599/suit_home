from class_creator import MyMQTTClass
import time
import random
import os

pid = os.getpid()
door = MyMQTTClass(pid)

while True:
    door_status = random.choice(['open', 'closed'])
    host = '127.0.0.1'
    topic = 'door/' + str(pid) + '/status'
    currentQoS = 2
    door.push_message(host, topic, currentQoS, door_status)
    time.sleep(5)