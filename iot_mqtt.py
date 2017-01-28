#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will subscribe and show all the messages sent by its companion
# awsiotpub.py using the AWS IoT hub

import paho.mqtt.client as paho
import os
import socket
import ssl
import requests
import json



sub_topic = '$aws/things/test_light/shadow/update/documents'
pub_topic = '$aws/things/test_light/shadow/update'

def gen_payload(status):
    return json.dumps({"state":{"reported":{"status":status}}})

def update_shadow(payload):
    mqttc.publish(pub_topic,payload)



def get_current_state():
    r = requests.get('http://127.0.0.1:8888/state')
    current_state = r.json()['state']
    return current_state


def actuate_thing(device,operation):
    endpoint='http://127.0.0.1:8888/{}/{}'.format(device,operation)
    print endpoint
    r = requests.get(endpoint)
    reported = r.json()['state']
    update_shadow(gen_payload(reported))






def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )
    update_shadow(gen_payload(get_current_state()))

def on_message(client, userdata, msg):
    if msg.topic == sub_topic:
        payload = json.loads(msg.payload)
        desired = payload['current']['state']['desired']['status']
        reported = payload['current']['state']['reported']['status']
        if desired != get_current_state():
            actuate_thing('light',desired)


        # import pdb; pdb.set_trace()

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "data.iot.eu-west-1.amazonaws.com"
awsport = 8883
# clientId = "myThingName"
# thingName = "myThingName"
caPath = "aws-iot-rootCA.crt"
certPath = "cert.pem"
keyPath = "privkey.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
