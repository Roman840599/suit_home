import paho.mqtt.client as mqtt
import sqlite3


id = 1
d = dict()


def on_message(client, userdata, msg):
    global id
    print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
    pid = msg.topic.split('/')[1]

    #Для того, чтобы начать передавать на сервер среднюю темпеатуру необходимо получить первое
    #сообщение от каждого градусника, которые помещаются в словарь d.
    d[pid] = int(msg.payload)
    if len(d) < 2:
        id += 1
        pass
    else:
        #Когда длина словаря соответствует числу градусников, начинает высчитываться среднее значение
        #и отправляется на сервер.
        sum = 0
        for i in d:
            sum += d[i]
        res = sum / 2
        print('start connection with server', res)
        try:
            cursor.execute("begin")
            cursor.execute("INSERT INTO main_sensor VALUES ({},{})".format(id, res))
            cursor.execute("commit")
        except:
            cursor.execute("rollback")
        id += 1


conn = sqlite3.connect("firstapp/db.sqlite3")
conn.isolation_level = None
cursor = conn.cursor()


client = mqtt.Client()
client.on_message = on_message
client.connect('127.0.0.1')
client.subscribe('thermometer/+/temperature', 0)
client.loop_forever()
