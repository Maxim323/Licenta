#Server
from flask import Flask, session, render_template, request, redirect, g, url_for, flash, Markup, jsonify, Response
from flask_socketio import SocketIO, emit, join_room, leave_room # pip install flask-socketio
import socket
import threading
import time
from extra import *

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__)
app.secret_key = "theCakeIsALie"

socketio = SocketIO(app, async_mode='eventlet')


def thread_function(x):
    while True:
        time.sleep(1)
        socketio.emit("randomNumber", {'number': giveMeRandom() }, namespace='/')

x = threading.Thread(target=thread_function, args=(1,))
x.start()


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('showMsgInConsole', namespace='/')
def streamControl(msg):
    print(msg) # print the message in console
    socketio.emit("showAlert", {'data': 'big booty bitches'}, namespace='/') #send an alert back to the server with a custom message


try:
    if __name__ == '__main__':
        socketio.run(app, host=IPAddr, port=1234, debug=True)

except BaseException as e:        
        print(e)
