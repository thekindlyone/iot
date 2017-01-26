from itertools import cycle                                                     
from flask import Flask, render_template ,jsonify                                       
import time



app = Flask(__name__)


pin = 3
state = False

mock = False

if not mock:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)                                                         
    GPIO.setup(pin, GPIO.OUT)                                                      

    

def actuate(desired,mock=False):
    global state
    if not mock:
        GPIO.output(pin, desired)
    state = desired
    

@app.route("/<device>/<operation>")                                                                 
def contol(device,operation):
    desired = {'on':True,'off':False}.get(operation)
    print state
    print desired
    # if desired == state:
    #     r= jsonify(response = 'redundant')

    # else:
    actuate(desired,mock=mock)
    print "----"
    print state
    print {True:'on',False:'off'}.get(state)
    r= jsonify(state = {True:'on',False:'off'}.get(state))
    # print r.content
    return r


@app.route('/state')
def getstate():
    return jsonify(state = {True:'on',False:'off'}.get(state))


@app.route('/')
def index():
    return 'Hello there'


if __name__ == "__main__":                                                      
    app.run(host='127.0.0.1',port =8888,debug=True)