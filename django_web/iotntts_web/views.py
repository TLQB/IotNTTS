from django.shortcuts import render
from paho.mqtt import client as mqtt_client
import random, json 
from .models import IotNTTSData,WarningData
from datetime import datetime
from django.http import JsonResponse 
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User

broker = 'broker.emqx.io'
port = 1883
topic = "iot"
client_id = f'python-mqtt-{random.randint(0, 100)}'
values,Username = None,None 


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global values 

        # print(json.loads(msg.payload))
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        values = json.loads(msg.payload)

        data = IotNTTSData.objects.create(thoi_gian= datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),  nhiet_do = int(values["ND"]),ph = int(values["PH"]),oxy = int(values["OXY"]))

        data.save()

        query_data = IotNTTSData.objects.all()

        if int(values["ND"]) > 100 or  int(values["PH"]) > 100 or  int(values["OXY"]) > 100:
            WarningData.objects.create(thoi_gian= datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), nhiet_do = int(values["ND"]),ph = int(values["PH"]),oxy = int(values["OXY"]))
        if len(query_data) > 2:
            IotNTTSData.objects.filter(id__in=list(IotNTTSData.objects.values_list('pk', flat=True)[:1])).delete()
            # print("delete success !")

    client.subscribe(topic)
    client.on_message = on_message

def publish(client,msg):

    result = client.publish("iot/control-motor",msg)

def handleConnect():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_start()
    except:
        return handleConnect()

handleConnect()


# Create your views here.
def home(requests):
    global Username
    if requests.user.is_staff or requests.user.is_superuser:
        Username = requests.user.username
        return render(requests,"home.html",{"Username":Username})
    else:
        return HttpResponseRedirect('/login')

def getData(requests):
	dataget = IotNTTSData.objects.all().order_by('-thoi_gian')[:5]
	return JsonResponse({"data":list(dataget.values())})

def dataWarning(requests):
    data_warning = WarningData.objects.all().order_by('-thoi_gian')
    return render(requests,"data-warning.html",{"data_warning":data_warning})

def controlMotor(requests):
    print("okk")

    return render(requests,"control-motor.html")

def settings(requests):

    return render(requests,"settings.html")

def manager(requests):
    users = User.objects.all()
    username = requests.POST.get("username_add")
    password = requests.POST.get("password_add")
    password_repeat = requests.POST.get("password_repeat")
    print(username,password,password_repeat,"///////////////")
    if password_repeat == password:
        try:
            user = User.objects.create_user(username=username,
                                     email=None,
                                     password=password_repeat)
            user.is_active = True 
            user.save()
        except:
            pass
    else:
        print("loiii ")


    return render(requests,"manager.html",{"users":users})

def login(requests):
    if requests.user.is_staff or requests.user.is_superuser:
        return HttpResponseRedirect("/data-realtime")

    username = requests.POST.get("username")
    password = requests.POST.get("password")

    user = authenticate(requests, username=username, password=password)
    if user:
        
        if user.is_active:
            try:
                login1(requests, user)
                return HttpResponseRedirect("/data-realtime") 
            except:
                print("loi")      
        else:           
            print("not ok")       
    else:  
        messages.error(requests, 'Error message here')
        return render(requests,"login.html",)

def logout(requests):
    logout1(requests)   
    return HttpResponseRedirect('/login')

def onoffmotor(requests):
    flag_motor = requests.POST['text']
    if flag_motor is not None:
        client = connect_mqtt()
        publish(client,flag_motor)
        print(flag_motor,"ok...")

    return HttpResponseRedirect('')