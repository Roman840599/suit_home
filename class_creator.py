import paho.mqtt.client as mqtt
import time
import random


class MyMQTTClass(mqtt.Client):
    def __init__(self, client_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id

    def res_of_connect(self, client, userdata, flags, rc):
        print("Result from connect: {}".format(mqtt.connack_string(rc)))

    def res_of_subscribe(self, client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(granted_qos[0]))

    def res_of_message(self, client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic,str(msg.payload)))

    def res_of_publish(self, client, userdata, mid):
        print(self.client_id, "mid: " + str(mid))

    mqtt.Client.on_connect = res_of_connect
    mqtt.Client.on_subscribe = res_of_subscribe
    mqtt.Client.on_message = res_of_message
    mqtt.Client.on_publish = res_of_publish

    def run(self, host_name, topic, QoS):
        self.connect(host_name)
        self.loop_start()
        while True:
            temperature = random.randrange(10, 30, 1)
            self.publish(topic, temperature, QoS)
            time.sleep(5)