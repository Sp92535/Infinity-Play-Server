from . import Blueprint, request, GameCardView

game_card_bp = Blueprint('game_card',__name__)
game_card_view = GameCardView()

@game_card_bp.route('/category_latest/<string:category>', methods = ['GET'])
def get_games_by_category(category):
    return game_card_view.get_games_by_category(category)

@game_card_bp.route('/category_all/<string:category>', methods = ['GET'])
def get_all_games_by_category(category):
    page_no = request.args.get('page_no', default=1, type=int)
    return game_card_view.get_all_games_by_category(category,page_no)

@game_card_bp.route('/search', methods = ['GET'])
def get_search_results():
    query = request.args.get('query', default='', type=str)
    page_no = request.args.get('page_no', default=1, type=int)
    return game_card_view.get_games_by_query(query,page_no)