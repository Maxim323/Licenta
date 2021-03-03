#Server
from flask import Flask, session, render_template, request, redirect, g, url_for, flash, Markup, jsonify, Response
from flask_socketio import SocketIO, emit, join_room, leave_room # pip install flask-socketio
import socket
from threading import Thread, Event



hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = Flask(__name__)
app.secret_key = "theCakeIsALie"

socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def _init_(self):
        self.delay = 1
        super(RandomThread, self)._init_()


    def randomNumberGenerator(self):



    def run(self):
        self.randomNumberGenerator()

thread = RandomThread()
        thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('showMsgInConsole', namespace='/')
def streamControl(msg):
    print(msg) # print the message in console
    socketio.emit("showAlert", {'data': 'big booty bitches'}, namespace='/') #send an alert back to the server with a custom message


if __name__ == '__main__':
    socketio.run(app, host=IPAddr, port=1234, debug=True)
