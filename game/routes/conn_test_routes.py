from . import Blueprint

conn_test_bp = Blueprint('conn_test',__name__)

@conn_test_bp.route('/',methods=['GET'])
def hello():
    return "Connection Successful Nigga.",200