from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from app.users import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from app.products import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

from app import views