from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..views.admin_view import AdminView
from ..views.game_card_view import GameCardView
from ..views.game_view import GameView