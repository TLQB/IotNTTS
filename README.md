A comprehensive IoT-based automation system for white leg shrimp farming utilizing LoRa technology and big data analytics. This project serves as the frontend interface for monitoring and controlling smart shrimp farming operations.

# Setup project 

1. Install lib requirements 
```shell
pip install -r requirements.txt 
```
2. Install mosquitto in linux open socket localhost
```shell
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
```
3. Install kivy, kivymd
```python
pip install kivy 
pip install kivymd 
```
# Run 
```python
python publish_1.py
python mobile_app/testApp.py
flask run 
```

