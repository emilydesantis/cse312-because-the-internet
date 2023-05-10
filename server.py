from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room,send
from flask_sqlalchemy import SQLAlchemy
import os
import html
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
       'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
room_user_count = {}
users_in_lobby = {}
words_to_guess = {}
game_state = {}




#--------------------------------------
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(100), unique=True, nullable=False)
   email = db.Column(db.String(100), unique=True, nullable=False)
   password = db.Column(db.String(100), nullable=False)
   salt = db.Column(db.String(100), nullable=False)


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
   username = session.get('username')
   #username = request.args.get('username')
   return render_template('page2.html', username=username)


@app.route('/page3/<room_name>', methods=['GET'])
def page3(room_name):
   #username = request.args.get('username')
   username = session.get('username')
   role = session.get('role')
   #role = request.args.get('role')
   return render_template('page3.html', room_name=room_name, username=username, role=role, game_state=game_state)


@app.route('/page4')
def page4():
   return render_template('page4.html')


@app.route('/lobby/<room_name>')
def lobby(room_name):
   username = session.get('username')
   #username = request.args.get('username')
   #escape html attack
   username = html.escape(username)
   print(username)
   print("------------------------------------")
   return render_template('lobby.html', room_name=room_name,username=username)


@app.route('/login', methods=['POST'])
def login():
   email = request.form.get('email')
   #escape html attack
   email = html.escape(email)
   password = request.form.get('password')
   #escape html attack
   password = html.escape(password)
   user = User.query.filter_by(email=email).first()
   bytes = password.encode('utf-8')
   pw = bcrypt.hashpw(bytes, user.salt)
   if user and user.password == pw:
       session['username'] = user.username
       render_template('page2',username=username)
       
   else:
       return "Login unsucessfull,incorrect username or password", 401
  


@app.route('/signup', methods=['POST'])
def signup():
   username = request.form.get('username')
   #escape html attack
   username = html.escape(username)
   email = request.form.get('email')
   #escape html attack
   email = html.escape(email)
   password = request.form.get('password')
   #escape html attack
   password = html.escape(password)
   #salt and hash password
   bytes = password.encode('utf-8')
   salt = bcrypt.gensalt()
   hashedPW = bcrypt.hashpw(bytes, salt)
   userN = User.query.filter_by(username=username).first()
   #print("username is")
   userE = User.query.filter_by(email=email).first()
   if not userN and not userE:
      new_user = User(username=username, email=email, password=hashedPW, salt=salt)
      db.session.add(new_user)
      db.session.commit()
      #print_all_users()
      session['username'] = username
      render_template('page2',username=username)
   else:
      return "Signup unsucessfull, duplicate username or email", 401


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
   room_user_count[room_name]=1
   emit('room_created', {'username': username, 'room_name': room_name}, room=room_name)
   emit('player_joined', {'username': username, 'room_name': room_name}, room=room_name)
   emit('navigate_to_lobby', {'room_name': room_name}, room=room_name)




@socketio.on('join_room')
def handle_join_room(data):
   username = data['username']
   room_name = data['room_name']
   if room_name not in room_user_count:
       return "room does not exists", 401
   else:
       emit('player_joined', {'username': username, 'room_name': room_name}, room=room_name)
       join_room(room_name)
       room_user_count[room_name] += 1  # Increment the user count for the room
       emit('navigate_to_lobby', {'room_name': room_name}, room=room_name)




      
@socketio.on('join_lobby')
def join_lobby(data):
   username = data['username']
   room_name = data['room_name']
   join_room(room_name)


   if room_name not in users_in_lobby:
       users_in_lobby[room_name] = []


   if username not in users_in_lobby[room_name]:
       users_in_lobby[room_name].append(username)


   emit('update_users_list', users_in_lobby[room_name], room=room_name)


@socketio.on('submit_word')
def handle_submit_word(data):
   room_name = data['room_name']
   word = data['word']
   #html escape
   word = html.escape(word)
   words_to_guess[room_name] = word
   game_state[room_name]['word'] = word
   game_state[room_name]['questions_left'] = 20
   emit('start_question_round', room=room_name)


@socketio.on('submit_question_or_guess')
def handle_submit_question_or_guess(data):
   room_name = data['room_name']
   question_or_guess = data['question_or_guess']
   #html escape
   question_or_guess = html.escape(question_or_guess)
   is_guess = data['is_guess']


   if is_guess:
       if question_or_guess.lower() == f"guess {game_state[room_name]['word'].lower()}":
           emit('game_over', {'result': 'win'}, room=room_name)
       else:
           game_state[room_name]['questions_left'] -= 1
           emit('display_question', {'question': question_or_guess}, room=room_name)
           emit('ask_for_answer', {'question': question_or_guess}, room=room_name)
           if game_state[room_name]['questions_left'] <= 0:
               emit('game_over', {'result': 'lose'}, room=room_name)
   else:
       game_state[room_name]['questions_left'] -= 1
       if game_state[room_name]['questions_left'] <= 0:
           emit('game_over', {'result': 'lose'}, room=room_name)
       else:
           emit('display_question', {'question': question_or_guess}, room=room_name)
           emit('ask_for_answer', {'question': question_or_guess}, room=room_name)
           


@socketio.on('submit_answer')
def handle_submit_answer(data):
   room_name = data['room_name']
   answer = data['answer']
   emit('disable_yes_no_buttons', room=room_name)
   emit('show_answer', {'answer': answer}, room=room_name)


@socketio.on('start_game')
def handle_start_game(data):
   room_name = data['room_name']
   game_state[room_name] = {
       'word': None,
       'questions_left': 20
   }
   emit('navigate_to_page3', {}, room=room_name)






@socketio.on('start_question_round')
def handle_start_question_round(data):
   room_name = data['room_name']
   emit('start_question_round', room=room_name)
   emit('disable_yes_no_buttons', room=room_name)




@socketio.on('correct_guess')
def handle_correct_guess(data):
   room_name = data['room_name']
   emit('game_over', {'result': 'win'}, room=room_name)








@socketio.on('select_role')
def handle_select_role(data):
   room_name = data['room_name']
   username = data['username']
   role = data['role']
   other_role = 'ask_questions' if role == 'select_word' else 'select_word'
  
   join_room(room_name)
  
   for user in users:
       if user['username'] != username:
           user['role'] = other_role
           emit('auto_assign_role', {'role': other_role, 'username': user['username']}, room=room_name)
          
   if role == 'select_word':
       emit('choose_word', room=room_name)


@socketio.on('hide_ask')
def handle_hide_ask(data):
   room_name = data['room_name']
   emit('ask_gone',room= room_name)


@socketio.on('hide_select')
def handle_hide_ask(data):
   room_name = data['room_name']
   emit('select_gone',room= room_name)





if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)


