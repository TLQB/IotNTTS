# 1 - The import
import PySimpleGUI as sg
import paho.mqtt.client as paho
broker = 'broker.emqx.io'
port = 1883
topic = "hung_message"
# 2 - Layout definition
layout = [  [sg.Text('My layout')],
            [sg.Input(key='-INPUT-')],
            [sg.Button('Send'), sg.Button('Cancel')] 
            ]
# 3 - Create window
window = sg.Window('Design Pattern 3 - Persistent Window', layout)
# 4 - Event Loop

def on_publish(client, userdata, result):
    print("data published")
    # log.debug("on_publish, mid {}".format(mid))
    print("************************")


client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker, port)

while True:
    event, values = window.read()


    if event in (None, 'Cancel'):
        break

    if event == "Send":
        msg = values["-INPUT-"]
        client1.publish(topic,msg)
        print(msg)

# 5 - Close window
window.close()