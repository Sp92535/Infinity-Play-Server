from . import Blueprint, request, jwt_required, AdminView

admin_bp = Blueprint('admin',__name__)
admin_view = AdminView()

@admin_bp.route('/create_user',methods=['POST'])
@jwt_required()
def create_user():
    return admin_view.create_user(request)

@admin_bp.route('/login',methods=['POST'])
def login():
    return admin_view.login(request)

@admin_bp.route('/search', methods=['GET'])
@jwt_required()
def find_user():
    username = request.args.get('username', default='', type=str)
    return admin_view.find_admin(username)

@admin_bp.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_user():
    username = request.args.get('username', default='', type=str)
    return admin_view.delete_admin(username)
