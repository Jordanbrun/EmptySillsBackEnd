import os
import models
from flask import Flask, request, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
from resources.plants import plant
from resources.users import user


DEBUG=True
PORT=8000

app = Flask(__name__)
CORS(plant)


app.secret_key = 'abjkduehdnsiau'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'testing things'

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')

CORS(plant, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(plant, url_prefix='/api/v1/plants')


CORS(app, origins=['http://localhost:3000'], supports_credentials=True)


if 'ON_HEROKU' in os.environ:
	print ('hitting os environ')
	models.initialize()

if __name__ == "__main__": 
    models.initialize()
    app.run(debug=DEBUG, port=PORT)