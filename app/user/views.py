from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route("/list")
def list():
    return 'hello world'