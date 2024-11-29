from flask import Flask
from flask_pymongo import MongoClient
from app.config import Config
from app.routes.orders import orders_blueprint
from app.routes.products import products_blueprint
from app.routes.main import main
from app.routes.cogs import cogs_blueprint
from app.routes.users import users_blueprint
from app.routes.feedbacks import feedbacks_blueprint

# Create the Flask app instance
def create_app():
    app = Flask(__name__)

    @app.template_filter('currency')
    def format_currency(value):
        try:
            return f"₱{value:,.2f}"
        except (ValueError, TypeError):
            return "₱0.00"
        
    app.config.from_object(Config)

    db = Config.db

    # Register blueprints for different routes
    app.register_blueprint(main)
    app.register_blueprint(orders_blueprint, url_prefix='/orders')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(cogs_blueprint, url_prefix='/cogs')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(feedbacks_blueprint, url_prefix='/feedbacks')

    app.db = db

    return app