from flask import Flask, render_template, request, session, redirect, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# SQLite database setup
conn = sqlite3.connect("chat.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS messages (room TEXT, sender TEXT, message TEXT, timestamp DATETIME)''')
conn.commit()

# User authentication
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            session['username'] = username
            return redirect('/chat')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return redirect('/')
    return render_template('register.html')

# Chat functionality
@app.route('/chat')
def chat():
    if 'username' in session:
        username = session['username']
        return render_template('chat.html', username=username)
    else:
        return redirect('/')

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    emit('join_room_announcement', f'{session["username"]} has entered the room.', to=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)
    emit('leave_room_announcement', f'{session["username"]} has left the room.', to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    sender = session['username']
    c.execute("INSERT INTO messages (room, sender, message, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (room, sender, message))
    conn.commit()
    emit('message', {'sender': sender, 'message': message}, to=room, include_self=False)

@socketio.on('get_messages')
def handle_get_messages(data):
    room = data['room']
    c.execute("SELECT sender, message FROM messages WHERE room=? ORDER BY timestamp", (room,))
    messages = c.fetchall()
    emit('load_messages', messages, to=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)