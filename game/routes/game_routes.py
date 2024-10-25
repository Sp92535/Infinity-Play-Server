from . import Blueprint, request, jwt_required, GameView

game_bp = Blueprint('game',__name__)
game_view = GameView()

@game_bp.route('/<string:game_name>', methods = ['GET'])
def get_game_by_name(game_name):
    return game_view.get_game_by_name(game_name)

@game_bp.route('/gameFile/<string:file_id>', methods = ['GET'])
def get_game_file_by_id(file_id):
    return game_view.get_game_file_by_id(file_id)

@game_bp.route('/admin/upload', methods=['POST'])
@jwt_required()
def upload_game():
    return game_view.upload_game(request)

@game_bp.route('/vote/<string:game_name>', methods=['GET'])
def vote_game(game_name):
    like = request.args.get('like', default=0, type=int)
    return game_view.vote_game(game_name,like)

@game_bp.route('/<string:game_name>', methods = ['DELETE'])
@jwt_required()
def delete_game_by_name(game_name):
    return game_view.delete_game_by_name(game_name)

@game_bp.route('/mail',methods=['POST'])
def send_report():
    return game_view.submit_report(request)
