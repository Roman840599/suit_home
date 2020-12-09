import paho.mqtt.client as mqtt
import asyncio
import websockets
from multiprocessing import Process, Queue
import sqlite3
import datetime


# Before writting down in db values of average temperature, we should recieve value of current temperature
# from each thermometer and put it down in some_dict. When the length of some_dict corresponds the amount
# of thermometers we can calculate average temperature by using get_average_temperature function and put
#  the result down in SQLite db.

some_dict = dict()

def get_average_temperature(dict):
    sum = 0
    for i in dict:
        sum += dict[i]
    res = sum / len(dict)
    return res


def serve_mqtt():

    def on_message(client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
        if msg.topic.startswith('sensor/door'):
            door_status = str(msg.payload).split("'")[1]
            q.put(door_status)
        elif msg.topic.startswith('sensor/thermometer'):
            pid = msg.topic.split('/')[2]
            if pid not in some_dict:
                some_dict[pid] = int(msg.payload)
            else:
                res = get_average_temperature(some_dict)
                some_dict[pid] = int(msg.payload)
                with sqlite3.connect("firstapp/db.sqlite3") as conn:
                    cursor = conn.cursor()
                    cursor.execute("begin")
                    current_time = datetime.datetime.now()
                    cursor.execute("INSERT INTO main_sensor VALUES (?, ?)", (current_time, res))
                    cursor.execute("commit")
        else:
            raise RuntimeError('topic name is incorrect')

    client.on_message = on_message
    client.loop_start()
    client.subscribe('sensor/#')


def serve_websocket():

    async def sending(websocket, path):
        while True:
            door_status = q.get()
            await websocket.send(door_status)

    specified_host = '127.0.0.1'
    specified_port = 5678
    start_server = websockets.serve(sending, specified_host, specified_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect("127.0.0.1")
    q = Queue()
    Process(target=serve_mqtt()).start()
    Process(target=serve_websocket()).start()




