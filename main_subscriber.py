import paho.mqtt.client as mqtt

d = dict()


def on_message(client, userdata, msg):
    print("Message received. Topic: {}. Payload: {}".format(msg.topic,str(msg.payload)))
    degree = msg.payload
    d[msg.topic] = int(degree)
    print(d)

    #вероятнее всего где-то здесь через subprocess.call вызывается скрипт создающий страничку
    # на локальном хосте, предположительно через CGI

client = mqtt.Client()
client.on_message = on_message
client.connect('127.0.0.1')
client.subscribe('thermometer/+/temperature', 0)
client.loop_forever()
