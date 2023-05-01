from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cse312-because-the-internet/templates/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/cse312-because-the-internet/templates/page3.html')
def page3():
    return render_template('page3.html')


@app.route('/cse312-because-the-internet/templates/page4.html')
def page4():
    return render_template('page4.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.errorhandler(404)
def not_found_error(error):
    return 'Error', 404
#--------------------------------------
#websocket handlers
@socketio.on('create_room')
def handle_create_room(data):
    username= data['username']
    room_name = data['room_name']
    join_room(room_name)
    emit('room_created', {'username': username, 'room_name': room_name}, room=room_name)

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room_name = data['room_name']
    join_room(room_name)
    emit('player_joined', {'username': username, 'room_name': room_name}, room=room_name)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, debug=True, allow_unsafe_werkzeug=True)
