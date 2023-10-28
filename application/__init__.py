from flask import Flask
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

cred = credentials.Certificate("SAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
annonce_ref = db.collection(u'annonces')
user_ref = db.collection(u'users')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)


# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from application.pages import views
from application.accounts import views
from application.annonces import views