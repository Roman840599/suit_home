import paho.mqtt.client as mqtt
import sqlite3

# In the SQLite3 db each new value of average temperature is related with unique id, which is foreign key.
# In this code mentioned id represented as id_of_average_temperature.
# In addition, before writting down in db values of average temperature,  we should recieve values
# of current temperature from each thermometer and put it down in some_dict.

id_of_each_average_temperature = 1
some_dict = dict()
number_of_thermometers = 2


def on_message(client, userdata, msg):
    global id_of_each_average_temperature
    print("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload)))
    pid = msg.topic.split('/')[1]
    some_dict[pid] = int(msg.payload)
    if len(some_dict) < number_of_thermometers:
        id_of_each_average_temperature += 1
        pass
    else:
        sum = 0  		# When the length of some_dict corresponds the amount of thermometers we can calculate
        for i in some_dict:  	# average temperature and put in down in db.
            sum += some_dict[i]
        res = sum / 2
        with sqlite3.connect("firstapp/db.sqlite3") as conn:
            cursor = conn.cursor()
            cursor.execute("begin")
            cursor.execute("INSERT INTO main_sensor VALUES ({},{})".format(id_of_each_average_temperature, res))
            cursor.execute("commit")
        id_of_each_average_temperature += 1


client = mqtt.Client()
client.on_message = on_message
client.connect('127.0.0.1')
client.subscribe('thermometer/+/temperature', 0)
client.loop_forever()
