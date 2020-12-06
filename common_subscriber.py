import paho.mqtt.client as mqtt
import asyncio
import websockets
from multiprocessing import Process, Queue
import sqlite3
import sys


# In the SQLite3 db each new value of average temperature is related with unique id, which is foreign key.
# In this code mentioned id represented as id_of_average_temperature.
# In addition, before writting down in db values of average temperature,  we should recieve values
# of current temperature from each thermometer and put it down in some_dict.


id_of_each_average_temperature = 1
some_dict = dict()
number_of_thermometers = int(sys.argv[1])   # when use runner.py.


def recieving_from_mqbroker():

    def on_message(client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
        if msg.topic.startswith('door'):
            print('work with door')
            door_status = str(msg.payload).split("'")[1]
            q.put(door_status)
        else:
            print('work with thermometer')
            global id_of_each_average_temperature
            pid = msg.topic.split('/')[1]
            some_dict[pid] = int(msg.payload)
            if len(some_dict) < number_of_thermometers:
                id_of_each_average_temperature += 1
                pass
            else:
                sum = 0                 # When the length of some_dict corresponds the amount of thermometers we
                for i in some_dict:     # can calculate average temperature and put in down in db.
                    sum += some_dict[i]
                res = sum / number_of_thermometers
                with sqlite3.connect("firstapp/db.sqlite3") as conn:
                    cursor = conn.cursor()
                    cursor.execute("begin")
                    cursor.execute("INSERT INTO main_sensor VALUES ({},{})".format(id_of_each_average_temperature, res))
                    cursor.execute("commit")
                id_of_each_average_temperature += 1

    client.on_message = on_message
    client.loop_start()
    client.subscribe([('door/+/status', 2), ('thermometer/+/temperature', 0)])


def sending_to_django():

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
    Process(target=recieving_from_mqbroker()).start()
    Process(target=sending_to_django).start()




