import os
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect
from flask_cors import CORS
from dotenv import load_dotenv
from .routes.admin_routes import admin_bp
from .routes.game_card_routes import game_card_bp
from .routes.game_routes import game_bp

app = Flask(__name__)
load_dotenv()

app.config['DEBUG'] = os.getenv('DEBUG') =='True'
app.config['PORT'] = int(os.getenv('FLASK_APP_PORT',80))
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Connect Database
try:
    connect(host=os.getenv('MONGO_HOST'))
except Exception as e:
    print(f'DATABASE CONNECTION FAILED {str(e)}')

# Enable Cross Origin Requests
CORS(app)

jwt = JWTManager(app)

# Register routes
app.register_blueprint(game_card_bp, url_prefix = '/api')
app.register_blueprint(game_bp, url_prefix = '/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')