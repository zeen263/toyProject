# environment : ESP32 (micropython)

from time import sleep
from lib.simple import MQTTClient
from machine import Pin
import network



def sub_cb(topic, msg):  # 이벤트 콜백처럼 동작

  message_decoded = msg.decode("utf-8")
  topic_decoded = topic.decode("utf-8")

  print("topic : " + topic_decoded + "message : " + message_decoded)

  if topic_decoded == "LED":
    if m == "on":
      led.value(1)
    elif m == "off":
      led.value(0)
    else:
      print("toggle")
      if led.value() == 0:
        led.value(1)
      else:
        led.value(0)


def esp32_publish():
  topic = "# TOPIC #"

  data1 = "# SENSOR DATA #"
  data2 = "# SENSOR DATA #"
  
  msg = data1 + "," + data2
  
  client.publish(topic, msg)
  print("published! topic : {0}, message : {1}".format(topic, message))
 


led = Pin(2, Pin.OUT, value = 0)

name="# YOUR WIFI #"; password="# YOUR PASSWORD #"
address="# YOUR DEVICE(ESP32) IP ADDRESS #"
device_ID="# YOUR DEVICE(ESP32) ID #"

wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(name,password)

if wifi.isconnected() == True:
  print("===== connected with " + name + "! =====")
  client = MQTTClient(device_ID, address)
  client.connect()

  while True:
    try:
      client.wait_msg()
    except:
      print("error")

    sleep(0.1)
  
else:
  print("not connected")
  sleep(1)


