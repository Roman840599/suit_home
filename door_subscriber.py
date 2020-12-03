import paho.mqtt.client as mqtt
import asyncio
import websockets
from multiprocessing import Process, Queue


def recieving_from_mqbroker():

    def on_message(client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
        door_status = str(msg.payload).split("'")[1]
        q.put(door_status)

    client.on_message = on_message
    client.loop_start()
    client.subscribe('door/+/status', 2)


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