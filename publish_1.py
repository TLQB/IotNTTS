# import paho.mqtt.client as paho
# import time
# import random

# broker = "broker.emqx.io"
# port = 1883


# def on_publish(client, userdata, result):
#     print("data published")
#     # log.debug("on_publish, mid {}".format(mid))
#     print("************************")


# client1 = paho.Client("control1")
# client1.on_publish = on_publish
# client1.connect(broker, port)

# while True:
#     client1.publish("tlqb/PH", random.randint(40, 90))
#     # client1.publish("tlqb/ND", random.randint(20, 40))
#     # client1.publish("tlqb/OXY", random.randint(20, 90))
#     time.sleep(5)
# """
# client1.publish("tlqb/PH", random.randint(40, 90))
# client1.publish("tlqb/ND", random.randint(20, 40))
# client1.publish("tlqb/OXY", random.randint(20, 90))
# client1.loop_forever()
# """

import random
import time

from paho.mqtt import client as mqtt_client
import json

broker = 'broker.emqx.io'
port = 1883
topic_PH = "tlqb/PH"
topic_ND = "tlqb/ND"
topic = "iot"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        # msg_PH = f"PH: {random.randint(40, 90)}"
        # msg_ND = f"ND: {random.randint(40, 90)}"
        msg = json.dumps({"PH":random.randint(40, 90),"ND":random.randint(40, 90),"OXY":random.randint(40, 90)})
        result = client.publish(topic,msg)
        # result_ND = client.publish(topic_ND, msg_ND)
        # status = result[0]
        # if status == 0:
        #     print(f"Send `{msg}` to topic `{topic}`")
        # else:
        #     print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count == 20:
            msg = json.dumps({"PH":15,"ND":200,"OXY":random.randint(40, 90)})
            result = client.publish(topic,msg)            


            msg_count = 0
            
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
