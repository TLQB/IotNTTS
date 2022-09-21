from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivy.uix.screenmanager import Screen,ScreenManager
from paho.mqtt import client as mqtt_client

from kivy.core.window import Window
Window.size = (350, 650)

from kivy.clock import Clock
import random
import json 

broker = 'broker.emqx.io'
port = 1883
topic_PH = "tlqb/PH"
topic_ND = "tlqb/ND"
topic ="iot"
client_id = f'python-mqtt-{random.randint(0, 100)}'
value = "default"
Builder.load_string('''
<Login>:
    Label:
        text: "LOGIN"
        color : 1,0,0,1
        size_hint: (1,0.1)
        pos_hint: {"center_x":0.5,"center_y":0.95}    
        color: 0,0,1,1    
    MDTextField:
        id : email_login
        hint_text: "Email"
        size_hint: (0.6,0.1)
        pos_hint: {"center_x":0.5,"center_y":0.7}

    MDTextField:
        id : password_login
        hint_text: "Password"
        password: True
        size_hint: (0.6,0.1)
        pos_hint: {"center_x":0.5,"center_y":0.6}
    MDFillRoundFlatButton:
        text:"Login"
        size_hint: (0.6,0.06)
        pos_hint: {"center_x":0.5,"center_y":0.4}

        on_press:root.login()

    MDFillRoundFlatButton:
        text:"Create Account"
        size_hint: (0.6,0.06)
        pos_hint: {"center_x":0.5,"center_y":0.3}

        on_press: root.manager.current = "signup"
    MDFillRoundFlatButton:
        text:"Forget Password"
        size_hint: (0.6,0.06)
        pos_hint: {"center_x":0.5,"center_y":0.2}

        on_press: root.manager.current = "fgp"
<Main>:

	FloatLayout:
		Label:
			text: "Độ PH :"
			color: "red"
			pos_hint: {"center_x":0.2,"center_y": 0.8}
		Label:
			id : ph_value
			text: "loading..."
			color: "red"
			pos_hint: {"center_x":0.6,"center_y": 0.8}


		Label:
			text: "Nhiệt độ :"
			color: "red"
			pos_hint: {"center_x":0.2,"center_y": 0.6}

		Label:
			id : nd_value
			text: "loading..."
			color: "red"
			pos_hint: {"center_x":0.6,"center_y": 0.6}


		Label:
			text: "% Oxy trong nước :"
			color: "red"
			pos_hint: {"center_x":0.2,"center_y": 0.4}

		Label:
			id : oxy_value
			text: "loading..."
			color: "red"
			pos_hint: {"center_x":0.6,"center_y": 0.4}

	''')
class Login(Screen):
	def login(self):

		self.manager.current = "main"
class Main(Screen):
    def update_value(self,*agrs):

        global value
        def connect_mqtt() -> mqtt_client:
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("Connected to MQTT Broker!")
                else:
                    print("Failed to connect, return code %d\n", rc)        
            client = mqtt_client.Client(client_id)
            client.on_connect = on_connect
            client.connect(broker, port)
            return client        
        

        def subscribe(client: mqtt_client):
            global value 
            def on_message(client, userdata, msg):
                # print(msg.payload.decode())
                # value = msg.payload.decode()
                print(msg.payload)
                value = json.loads(msg.payload)
                self.ids['ph_value'].text = str(value["PH"])
                self.ids['nd_value'].text = str(value["ND"])
                self.ids['oxy_value'].text = str(value["OXY"])
                print(value,"****************")


            # client.subscribe(topic_PH)
            # client.subscribe(topic_ND)
            client.subscribe(topic)
            client.on_message = on_message

        client = connect_mqtt()
        subscribe(client)
        client.loop_start()

        
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        Clock.schedule_once(self.update_value,5)

class testApp(MDApp):
    def build(self):
        sm  = ScreenManager()
        sm.add_widget(Login(name = "login"))
        sm.add_widget(Main(name = "main"))
        return sm 

    # def on_start(self):
    #     global value
    #     def connect_mqtt() -> mqtt_client:
    #         def on_connect(client, userdata, flags, rc):
    #             if rc == 0:
    #                 print("Connected to MQTT Broker!")
    #             else:
    #                 print("Failed to connect, return code %d\n", rc)        
    #         client = mqtt_client.Client(client_id)
    #         client.on_connect = on_connect
    #         client.connect(broker, port)
    #         return client        
        

    #     def subscribe(client: mqtt_client):
    #         global value 
    #         def on_message(client, userdata, msg):
    #             print(msg.payload.decode())
    #             value = msg.payload.decode()
    #             print(value,"****************")

    #         client.subscribe(topic)
    #         client.on_message = on_message

    #     client = connect_mqtt()
    #     subscribe(client)
    #     client.loop_start()


testApp().run()



# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.garden.navigationdrawer import NavigationDrawer
# from kivy.properties import StringProperty
# import paho.mqtt.client as mqtt

# class Drawer(NavigationDrawer):
#     vartext1 = StringProperty("Button")
#     vartext2 = StringProperty("Text")

# class MainMenuApp(App):
#     def build(self):
#         return Drawer()

#     def on_start(self):
#         topic = "tlqb/PH"

#         def onConnect(client, userdata, flags, rc):
#             mqttc.subscribe(topic, 0)

#         def onMessage(client, userdata, msg):
#             msg.payload = msg.payload.decode("utf-8")
#             print ("[INFO   ] [MQTT        ] topic: " + msg.topic +" msg: "+ msg.payload)

#             if msg.topic == "tlqb/PH":
#                 userdata['self'].root.vartext2 = msg.payload

#         parameters = {'self': self}
#         mqttc = mqtt.Client(client_id="kivy-client", clean_session=True, userdata = parameters)
#         mqttc.on_connect      = onConnect 
#         mqttc.on_message      = onMessage
#         mqttc.connect('broker.emqx.io', 1883, keepalive=60, bind_address="")
#         mqttc.loop_start() # start loop to process callbacks! (new thread!)

# if __name__ == "__main__":
#     MainMenuApp().run()