import paho.mqtt.client as mqttClient
import time


def save_msg(temp_data):
    with open("cabresto_temp.txt", "a+") as f:
        f.write(temp_data.decode("utf-8")  + "\n")


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    try:
        print(message.payload)
        save_msg(message.payload)

    except Exception as e:
        print(e)

Connected = False
broker_address = "localhost"
port = 1883
user = "cabresto_01"
password = "segredo"
id_client = "Joao"

client = mqttClient.Client(id_client)
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)

client.loop_start()

while Connected is not True:
    time.sleep(0.1)

client.subscribe("labmet/cabresto_01/temperature/#")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
