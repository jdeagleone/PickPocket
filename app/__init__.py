from flask import Flask, render_template
from flask.ext.session import Session

app = Flask(__name__)
app.config.from_object('config')
Session(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


from app.auth_module import views
