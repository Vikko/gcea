"""
 Global configuration
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Create secret for forms
app.config['SECRET_KEY'] = '0123456789abcdef'  # Not very secret, but functional
# Setup db link
db_file = "pokemon.db"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../gcea/{db_file}'  # Put the db in the root instead of instance folder

db = SQLAlchemy(app)

from gcea import routes
