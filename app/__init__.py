from flask import Flask
from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password' 

csrf = CSRFProtect(app) 

from app.users import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from app.products import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

from app import views

