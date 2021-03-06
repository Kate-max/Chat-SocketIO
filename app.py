#!pip install ajax
#!pip install stackpath
#console.log("string") html
from flask import Flask, render_template, url_for, redirect, session, request
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

from pytz import timezone
from datetime import datetime
UTC = timezone('UTC')
def time_now():
    return datetime.now(UTC)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_string'

socketio = SocketIO(app, cors_allowed_origins='*')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://OAS_Manager:OAS@localhost/flask'
#postgresql://сервер:пароль@localhost/таблица
db = SQLAlchemy(app)


class ChatMessages(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    msg      = db.Column(db.Text)
    date     = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.msg

# запись в бд
@socketio.on('message')
def handleMessage(data):
    print(f"Message: {data}")
    send(data, broadcast=True) # вывод сообщений в разных браузерах

    message = ChatMessages(username=data['username'], msg=data['msg'], date = time_now())
    db.session.add(message)
    db.session.commit()


@app.route('/')
def index():
    print(session) # сессия
    username = None
    if session.get("username"):
        username = session.get("username")
    return render_template('index.html', username=username)


# вход
@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
    return redirect(url_for('index'))

# выход
@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    socketio.run(app)
    #app.run()
    exit()
