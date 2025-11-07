from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    from app.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    from app.products import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')
    
    from app.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/post')
    
    from app.views import register_routes
    register_routes(app)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    return app