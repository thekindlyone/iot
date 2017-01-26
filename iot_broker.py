import boto3
import requests
import time
import json

client = boto3.client('iot-data')
# q1 = sqs.get_queue_by_name(QueueName='requestqueue')
# q2 = sqs.get_queue_by_name(QueueName='responsequeue')

def gen_payload(status):
    return json.dumps({"state":{"reported":{"status":status}}})




def update_shadow(payload):
    client.update_thing_shadow(thingName="test_light",payload=payload)

def get_shadow():
    res=client.get_thing_shadow(thingName="test_light")
    payload = json.loads(res['payload'].read())
    return payload['state'].get('desired',{}).get('status') 
    # return payload['state']['reported']



def actuate_thing(device,operation):
    endpoint='http://127.0.0.1:8888/{}/{}'.format(device,operation)
    print endpoint
    r = requests.get(endpoint)
    reported = r.json()['state']
    update_shadow(gen_payload(reported))


def get_current_state():
    r = requests.get('http://127.0.0.1:8888/state')
    current_state = r.json()['state']
    return current_state



while True:
    desired = get_shadow() 
    reported = get_current_state()
    if desired and desired != reported:
        print "desired = {}   reported = {}".format(desired,reported)
        actuate_thing("light",desired)
    time.sleep(2)
        # import pdb; pdb.set_trace()
