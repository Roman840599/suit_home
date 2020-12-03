import paho.mqtt.client as mqtt
import asyncio
import websockets
from multiprocessing import Process, Queue


def recieving_from_mqbroker():

    def on_message(client, userdata, msg):
        print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
        q.put(str(msg.payload))

    client.on_message = on_message
    client.loop_start()
    client.subscribe('door/+/status', 2)


def sending_to_django():

    async def sending(websocket, path):
        while True:
            m = q.get()
            if m == "b'0'":
                await websocket.send('closed')
            else:
                await websocket.send('open')

    start_server = websockets.serve(sending, '127.0.0.1', 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect("127.0.0.1")
    q = Queue()
    Process(target=recieving_from_mqbroker()).start()
    Process(target=sending_to_django).start()