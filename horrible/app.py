from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from random import randint
import redis
import atexit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
db = redis.StrictRedis(host="localhost", port=6379, db=0)

@socketio.on('connect')
def connect():
    print('connected!')

@socketio.on('disconnect')
def disconnect():
    print('disconnected!')

    room = db.get(f'room:{request.sid}')
    if room is not None:
        delete_player(room.decode(), request.sid)
        return None
    room = db.get(f'host:{request.sid}')
    if room is not None:
        delete_host(room.decode(), request.sid)
        return None
    print('Session did not have a corresponding player/host')

def delete_host(room, sid):
    result = [
        db.delete(f'host:{sid}'),
        (db.srem('open_game', room) or db.srem('started_game', room)),
    ]
    emit('quit', room=room)
    if all(result):
        print('deleted host from room', room, sid)
    else:
        print('error deleting host from room', room, sid, result)
    for playersid in db.smembers(f'player:{room}'):
        delete_player(room, playersid.decode())

def delete_player(room, sid):
    result = [
        db.delete(f'room:{sid}'),
        db.srem(f'player:{room}', sid),
    ]
    if all(result):
        print('deleted player from room', room, sid)
    else:
        print('error deleting player from room', room, sid, result)
    delete_question(room, sid)

def delete_question(room, sid):
    result = db.delete(f'question:{room}:{sid}')
    db.delete(f'answer:{room}:{sid}')
    if (result):
        print('deleted question', room, sid)
    else:
        print('no question deleted', room, sid)
        
@socketio.on('join')
def join(json):
    username = json['username']
    room = json['room']
    print('joining room...', room, username, request.sid)
    if (db.sismember('open_game', room)
        and db.sadd(f'player:{room}', request.sid)
        and db.set(f'room:{request.sid}', room)):
        join_room(room)
        print('joined room', room, username)
        emit('joined', username, room=room)
    else:
        print('no matching game', room)

@socketio.on('create_game')
def create_game():
    print('creating game...', request.sid)
    room = None
    while room is None or not db.sadd('open_game', room):
        room = ''.join([str(randint(0, 9)) for i in range(4)])
    print('game created', room)
    db.set(f'host:{request.sid}', room)
    join_room(room)
    emit('game_created', room, room=room)

@socketio.on('start_game')
def start_game(room):
    print('starting game...', room)
    if db.srem('open_game', room) and db.sadd('started_game', room):
        emit('game_started', room=room)
        print('game started', room)

@socketio.on('get_question')
def get_question(room):
    question = 'a question!'
    print('getting question', room, request.sid, question)
    db.sadd(f'question:{room}:{request.sid}', question)
    emit('question', question)
    
@socketio.on('answer')
def answer(room, answer):
    print('answer recieved', room, answer)
    db.set(f'answer:{room}:{request.sid}', answer)
    answers = []
    for sid in db.smembers(f'player:{room}'):
        answer = db.get(f'answer:{room}:{sid.decode()}')
        if answer is None:
            return None
        answers.append(answer.decode())
    print('all answers recieved, starting', answers)
    emit('start_answers', answers, room=room)

@socketio.on('get_questions')
def get_questions(room):
    if db.get(f'host:{request.sid}').decode() != room:
        print('error getting questions is for the host of the room', room)
        return None
    result = []
    for playersid in db.smembers(f'player:{room}'):
        question = db.get(f'question:{room}:{playersid.decode()}').decode()
        result.append(question)
    return result
    
@app.route('/')
def index():
    return render_template('index.jinja')

if __name__ == '__main__':
    # make sure that the database is clean on each restart
    #   to prevent leaks
    def cleanup():
        try:
            db.flushall()
            print('flushed database')
        except Exception:
            print('error flushing database')

    atexit.register(cleanup)

    socketio.run(app)
