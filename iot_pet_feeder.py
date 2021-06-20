import machine
import time, urandom
import ssd1306 #display screen library
from machine import Pin, I2C, PWM #to configure pins of sensors
#display pins configuration
i2c = I2C(-1, scl=Pin(22), sda=Pin(21), freq=100000)
disp = ssd1306.SSD1306_I2C(128, 64, i2c)
#displaying text
disp.fill(0)
disp.text("Connecting to", 0, 20)
disp.text("internet...", 0, 40)
disp.show()
time.sleep(1)

#To connect to the internet
import network
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.connect('wifi-name', 'wifi-password') # connect to an AP
wlan.config('mac')      # get the interface's MAC address
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
if (wlan.isconnected == False):
    print('Connection unsuccessful')
    disp.fill(0)
    disp.text("Connection", 20, 20)
    disp.text("Failed!", 20, 40)
    disp.show()
    time.sleep(1)
else:
    print('Connection successful')
    disp.fill(0)
    disp.text("Connection", 20, 20)
    disp.text("successful!", 20, 40)
    disp.show()
    time.sleep(1)

disp.fill(0)
disp.text("Connecting with", 0, 20)
disp.text("MQTT Broker", 20, 40)
disp.show()
time.sleep(1)
#Connecting MQTTClient
from umqtt.simple import MQTTClient
server = 'mqtt.thingspeak.com'
c = MQTTClient('ESP32_danial', server, ssl=True) #ssl=True mean TLS is enabled
c.connect()

#Thingspeak credentials
CHANNEL_ID = ""
API_KEY = "" #Write API Key from Thingspeak
topic = "channels/" + CHANNEL_ID + "/publish/" + API_KEY

print('Configuring I/O pins')
disp.fill(0)
disp.text("Configuring",20, 20)
disp.text("I/O pins", 20, 40)
disp.show()
time.sleep(1)
from hcsr04 import HCSR04 #sonar library
time.sleep(1)
#sonar pins
sonar = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=1000000)
#servo pins
p14 = machine.Pin(14)
servo = machine.PWM(p14,freq=50,duty=77)


#for listening to thingspeak
#import urllib2
#import json #not installing

print('Starting while loop')
while True: 
    distance = sonar.distance_cm()
    print('Sonar distance: ', distance)
    disp.fill(0)
    disp.text("Sonar distance: ", 0, 20)
    disp.text(str(distance), 30, 40)
    disp.show()
    time.sleep(2)
    
    if (distance <= 20): #change this to > instead of <
        print("Plate is empty!")
        disp.fill(0)
        disp.text("Plate is empty!", 0, 20)
        disp.text("Refilling...", 0, 40)
        disp.show()
        time.sleep(1)
        #Refilling the plate
        servo.duty(20)
        time.sleep(1)
        print('Rotating')
        servo.duty(127)
        time.sleep(2)
        print('Rotating back')
        servo.duty(20)
        time.sleep(1)
        print("Plate filled")
        disp.fill(0)
        disp.text("Plate refilled!", 0, 30)
        disp.show()
        time.sleep(1)
    else:
        print("Food not finished")
        disp.fill(0)
        disp.text("Plate is full", 0, 30)
        disp.show()
        time.sleep(1)
    
    print('Publishing information')
    disp.fill(0)
    disp.text("Publishing info", 0, 30)
    disp.show()
    time.sleep(1)
        
    #Publishing information on mqtt broker
    dst = "field1="+str(distance) #sonar distance
    #c.publish(topic, fld1)
    if (distance <= 20):
        msg = 'Plate is empty!\nRefilling...'
    else:
        msg = 'Plate is full!'
    
    #msg = " " + str(msg)
    #combined = dst + msg
    time.sleep(10)
    c.publish(topic, dst)
    
    print('Data published on broker')        
    disp.fill(0)
    disp.text("Published!", 0, 30)
    disp.show()
    time.sleep(1)
    #to read data from thingspeak
#       print('listening to thingspeak')
#       read_api = '9P3W6DR4JAJSOZNE'
#       channel_id = '1349736'
#       TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
#                        % (CHANNEL_ID,READ_API_KEY))
#       response = TS.read()
#       data=json.loads(response)
#       a = data['field1']
#       print('data received: ')
#       print (a)
#       time.sleep(1)   
#       TS.close()
    time.sleep(1)



