from flask import Flask, render_template
from flask_session import Session
from flask_script import Shell, Manager
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object('config')
Session(app)
manager = Manager(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


def make_shell_context():
    return dict(app=app)


manager.add_command('shell', Shell(make_shell_context))

from app.auth_module import views
