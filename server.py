from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
room_user_count = {}


#--------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

#----------------------------------------------------
#debugging
def print_all_users():
    users = User.query.all()
    for user in users:
        print(user)
#-----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    username = request.args.get('username')
    return render_template('page2.html', username=username)

@app.route('/page3/<room_name>')
def page3(room_name):
    username = request.args.get('username')
    return render_template('page3.html', room_name=room_name, username=username)

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/lobby/<room_name>')
def lobby(room_name):
    username = request.args.get('username')
    return render_template('lobby.html', room_name=room_name,username =username)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        return redirect(url_for('page2', username=user.username))
    else:
        return "Login unsucessfull,incorrect username or password", 401
    

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    print_all_users()
    return redirect(url_for('page2',username=username))

@app.errorhandler(404)
def not_found_error(error):
    return 'Error', 404

#--------------------------------------
#websocket handlers


@socketio.on('create_room')
def handle_create_room(data):
    username = data['username']
    room_name = data['room_name']
    join_room(room_name)
    if room_name not in room_user_count:
        room_user_count[room_name] = 1
    emit('room_created', {'username': username, 'room_name': room_name}, room=room_name)
    emit('navigate_to_lobby', {'username': username,'room_name': room_name})

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room_name = data['room_name']
    if room_name not in room_user_count:
        return "room does not exists", 401
    else:
        emit('player_joined', {'username': username, 'room_name': room_name}, room=room_name)
        join_room(room_name)
        room_user_count[room_name] += 1

    # Start the game once the second player arrives
    print("--------------------------------------")
    print(room_user_count[room_name])
    if room_user_count[room_name] == 2:
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        emit('start_game', {'username': username}, room=room_name)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print_all_users()
        print("--------------------------------------")
        print("/r/n/r/n")
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)
