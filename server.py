from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room
app = Flask(__name__, template_folder= 'frontend')
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading.js')
def loading_js():
    return app.send_static_file('loading.js')

@app.route('/style.css')
def style_css():
    return app.send_static_file('style.css')

@app.errorhandler(404)
def not_found_error(error):
    return 'Error', 404

@socketio.on('join')
def on_join(user_data):
    username = user_data['username']
    room = user_data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(user_data):
    username = user_data['username']
    room = user_data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)