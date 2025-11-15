from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghostcord'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

users = {}

@app.route('/')
def index():
    return 'GhostCord Backend Live'

@socketio.on('add user')
def add_user(username):
    users[request.sid] = username
    emit('login', {'users': list(users.values())}, broadcast=True)

@socketio.on('new message')
def new_message(data):
    emit('new message', {'username': data['username'], 'message': data['message']}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    if request.sid in users:
        username = users.pop(request.sid)
        emit('user left', {'username': username, 'users': list(users.values())}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
