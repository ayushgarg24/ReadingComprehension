import time
import test
from flask import Flask, request


app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route("/")
def home():
    return test.some_func()

@app.route('/record', methods=['POST','GET'])
def MuseRecording():
    
    if request.method == 'POST':
        # RUN RECORDING FUNCTION HERE 
        # 
        return test.post_func(10)

    if request.method == 'GET':
        # STOP RECORDING, RETURN JSONIFIED DATA
        return test.get_func()
    else:
        return "Method Not Allowed"



