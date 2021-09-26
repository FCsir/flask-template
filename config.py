import os
import redis

class BaseConfig:  # 基本配置类
    SECRET_KEY = 'wZ9mAQgA2oaGn94z85uJXalvNPXmzTArP6lD0ZQOdj5ql0uoi0DLTryTCcI='
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost:3306/gtrading'
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # session 的有效期，单位是秒
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DevelopmentConfig(BaseConfig):  #  开发环境
    DEBUG = True
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/gtrading_bian?charset=utf8'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_recycle':3600}
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_TIMEOUT = 120


class TestingConfig(BaseConfig):  # 测试环境
    DEBUG = False

class ProductionConfig(BaseConfig):  # 生产环境
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product': ProductionConfig,
    'default': DevelopmentConfig
}