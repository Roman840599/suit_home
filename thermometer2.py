from class_creator import MyMQTTClass
import os

pid = os.getpid()
thermometer = MyMQTTClass(str(pid))

# run(host_name, topic, QoS)
thermometer.run('127.0.0.1', 'thermometer/02/temperature', 0)