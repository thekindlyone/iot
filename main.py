from flask import Flask, render_template
from flask_ask import Ask, statement
import boto3
import json
import time
# sqs = boto3.resource('sqs')
# req_q = sqs.get_queue_by_name(QueueName='requestqueue')
# res_q = sqs.get_queue_by_name(QueueName='responsequeue')

client = boto3.client('iot-data')

app = Flask(__name__)
ask = Ask(app, '/')



# @ask.intent('IlluminateIntent')
# def illuminate_handler(device,operation):
#     # text = "hello {}".format(firstname)
#     # print "Illuminated"
#     req_q.send_message(
#         MessageBody=json.dumps( 
#             dict(
#                 device = device,
#                 operation = operation
#                 )))
#     c = 0
#     while(True):
#         time.sleep(1)
#         c+=1
#         if c>30:
#             return statement('Operation timed out').simple_card('Timeout', 'Took too long')
#         for m in res_q.receive_messages():
#             print 'message body is',m.body
#             body = json.loads(m.body)
#             m.delete()
#             if body['response']== 'success':
#                 text = "Affirmative, {} is turned {}".format(device, operation)
#                 return statement(text).simple_card('Success', text)
#             elif body['response'] == 'redundant' :
#                 text = "Redundant, {} was already {}".format(device,operation)
#                 return statement(text).simple_card('Redundant', text)
                



def get_shadow():
    res=client.get_thing_shadow(thingName="test_light")
    payload = json.loads(res['payload'].read())
    return payload['state'].get('reported',{}).get('status')

def gen_payload(status):
    return json.dumps({"state":{"desired":{"status":status}}})


def update_shadow(payload):
    client.update_thing_shadow(thingName="test_light",payload=payload)


    
@ask.intent('ControlIntent')
def control_handler(device,operation):
    desired = operation
    reported = get_shadow()
    if reported == desired:
        text = "{} was already {}".format(device,operation)
        title = 'Redundant'
    else:
        text = "Your word is law. {} is now {}".format(device,operation)
        title = "Success"

    

    update_shadow(gen_payload(desired))
    return statement(text).simple_card(title, text)


if __name__ == '__main__':
    app.run(debug=True)