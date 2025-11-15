import os
import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO, emit, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghostcordv2'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

users = {}

@app.route('/')
def index():
    return 'GhostCord V2 Backend: ACTIVE & READY'

@socketio.on('add user')
def add_user(username):
    users[request.sid] = username
    emit('login', {'users': list(users.values())}, broadcast=True)
    emit('user joined', {'username': username, 'users': list(users.values())}, broadcast=True)

@socketio.on('new message')
def new_message(data):
    emit('new message', {'username': data['username'], 'message': data['message']}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    if request.sid in users:
        username = users.pop(request.sid)
        emit('user left', {'username': username, 'users': list(users.values())}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
