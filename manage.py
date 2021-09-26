import os
import redis
import sys
import logging
import pkgutil
from flask import Flask, request
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from config import config
from importlib import import_module
from common_utils.log_utils import MultiprocessHandler
from app.user.views import user_bp

from models import db

def load_custom_commands(app, manager):
    base_dir = app.config['BASE_DIR']
    command_dir = os.path.join(base_dir, 'command')
    commands = [name for _, name, is_pkg in pkgutil.iter_modules([command_dir]) if not is_pkg and not name.startswith('_')]
    for command in commands:
        module = import_module('command.%s' % command)
        manager.add_command(command, module.CustomCommand())

    return

def create_app():
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV')
    config_dict = config[env] 
    app.config.from_object(config_dict)

    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG)
    formattler = '%(asctime)s - thread-%(thread)-8d - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    fmt = logging.Formatter(formattler)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)

    log_name = "error"
    file_handler = MultiprocessHandler(log_name, when='D')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    app.log = logger

    @app.before_request
    def before_requests():
        logger.debug('\nip:%s,url:%s,begin..'% (request.remote_addr,request.url))

    @app.after_request
    def after_requests(response):
        logger.debug('\nip:%s,url:%s,end..\n'% (request.remote_addr,request.url))
        return response

    # 从config中读取redis服务器的配置
    host = app.config.get('REDIS_HOST')
    port = app.config.get('REDIS_PORT')
    db_redis = app.config.get('REDIS_DB')
    db_passwd = app.config.get('PASSWORD')
    app.redis_client = redis.StrictRedis(host=host, port=port, db=db_redis, password=db_passwd)

    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(user_bp, url_prefix='/user')
    db.init_app(app)
    CORS(app, supports_credentials=True)

    return app

app = create_app()
manager = Manager(app)
Migrate(app, db)
# attention: the command name no same
load_custom_commands(app, manager)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()