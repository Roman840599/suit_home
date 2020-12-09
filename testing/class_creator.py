import paho.mqtt.client as mqtt


class MyMQTTClass(mqtt.Client):

    def __init__(self, client_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.has_published = False

    def res_of_connect(self, client, userdata, flags, rc):
        print("Result from connect: {}".format(mqtt.connack_string(rc)))

    def res_of_subscribe(self, client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(granted_qos[0]))

    def res_of_message(self, client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic,str(msg.payload)))

    def res_of_publish(self, client, userdata, mid):
        if mid > 0:
            self.has_published = True

    def push_message(self, host_name, topic, QoS, message_to_publish):
        self.on_publish = self.res_of_publish
        self.connect(host_name)
        self.loop_start()
        self.publish(topic, message_to_publish, QoS)
        self.loop_stop()
