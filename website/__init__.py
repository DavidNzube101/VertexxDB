
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os.path import *
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "VDBSQLITE.db"

def initialize_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'LALAL23KMmlams2,laml;r#;"1'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///VDBSQLITE.db'

  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User

  create_db(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  @app.errorhandler(500)
  def internal_server_error(e):
      return render_template('broken-page.html'), 500

  return app

def create_db(the_app):
  db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
  if not isfile(db_path):
      with the_app.app_context():
          db.create_all()
      print("Database created!")

    