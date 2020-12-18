import paho.mqtt.client as mqtt
import time, traceback


class MyMQTTClass(mqtt.Client):

    def __init__(self, client_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(str(client_id)) == 0:
            raise RuntimeError('client id is incorrect')
        else:
            self.client_id = client_id
        self.messages = []
        self.publisheds = []
        self.on_connect = self.res_of_connect
        self.on_subscribe = self.res_of_subscribe
        self.on_message = self.res_of_message
        self.on_publish = self.res_of_publish

    def res_of_connect(self, client, userdata, flags, rc):
        # print("Result of connection: {}".format(mqtt.connack_string(rc)))
        pass

    def res_of_subscribe(self, client, userdata, mid, granted_qos):
        # print("I've subscribed with QoS: {}".format(granted_qos[0]))
        pass

    def res_of_message(self, client, userdata, msg):
        # print("Message received. Topic: {}. Payload: {}".format(msg.topic,str(msg.payload)))
        self.messages.append(msg.payload)

    def res_of_publish(self, client, userdata, mid):
        # print(self.client_id, "mid: " + str(mid))
        self.publisheds.append(mid)

    def push_message(self, host_name, port, topic, QoS, message_to_publish):
        self.connect(host_name, port)
        self.loop_start()
        self.publish(topic, message_to_publish, QoS, retain=False)
        time.sleep(2)
        self.loop_stop()
