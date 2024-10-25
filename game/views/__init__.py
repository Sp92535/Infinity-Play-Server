import base64
import hashlib
import bcrypt
import requests
import os
from bson import ObjectId
from flask import jsonify, Response
from mongoengine import DoesNotExist, Q, ValidationError
from werkzeug.exceptions import Unauthorized
from werkzeug.utils import secure_filename
from ..models.game_model import Game
from ..models.admin_model import Admin
from ..utils.bucket import get_bucket
from flask_jwt_extended import create_access_token, get_jwt_identity
from dotenv import load_dotenv

load_dotenv()