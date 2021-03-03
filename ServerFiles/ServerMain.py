#Server
from flask import Flask, session, render_template, request, redirect, g, url_for, flash, Markup, jsonify, Response
from flask_socketio import SocketIO, emit, join_room, leave_room # pip install flask-socketio
import eventlet
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


#eventlet.monkey_patch() #Fixes socketio message broadcasting from threads

app = Flask(__name__)
app.secret_key = "theCakeIsALie"

socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('showMsgInConsole', namespace='/')
def streamControl(msg):
    print(msg) # print the message in console
    socketio.emit("showAlert", {'data': 'big booty bitches'}, namespace='/') # send an alert back to the server with a custom message


if __name__ == '__main__':
    app.run(host=IPAddr, port=1234, debug=True)

