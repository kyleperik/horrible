from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from random import randint
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
db = redis.StrictRedis(host="localhost", port=6379, db=0)

@socketio.on('join')
def join(json):
    username = json['username']
    room = json['room']
    if db.sadd(f'room:{room}', username):
        join_room(room)
        emit('joined', username, room=room)

@socketio.on('create_game')
def create_game():
    room = None
    while room is None or db.sadd('open_game', room):
        room = ''.join([str(randint(0, 9)) for i in range(4)])
    join_room(room)
    emit('game_created', room, room=room)

@socketio.on('start_game')
def start_game(room):
    if db.srem('open_game:{room}') and db.sadd('started_game', room):
        emit('game_started', room=room)

@socketio.on('get_question')
def get_question(room, username):
    question = 'a question!'
    db.sadd('question:{room}:{username}', question)
    emit('question', question)
    
@socketio.on('set_answer')
def set_answer(room, username, answer):
    db.sadd('answer:{room}:{username}', answer)
    
@app.route('/')
def index():
    return render_template('index.jinja')

if __name__ == '__main__':
    socketio.run(app
)
