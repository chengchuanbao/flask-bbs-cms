import os
from datetime import timedelta
class BaseConfig:
    #数据库的配置
    MYSQL_DIALECT='mysql'
    MYSQKL_DRIVER='pymysql'
    MYSQL_NAME='root'
    MYSQL_PWD='123456'
    MYSQL_HOST='localhost'
    MYSQL_PORT='3306'
    MYSQL_DB='flask_bbs'
    MYSQL_CHARSET='utf8mb4'
    SQLALCHEMY_DATABASE_URI=f'{MYSQL_DIALECT}+{MYSQKL_DRIVER}://{MYSQL_NAME}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?{MYSQL_CHARSET}'
    SQlALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY  = os.urandom(16)
    SQlALCHEMY_TRACK_MODIFICATIONS = True

    #邮箱配置
    MAIL_SERVER = "smtp.163.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIl_USERNAME = "17839585182@163.com"
    #开启邮箱smtp服务时自动生成的授权密码
    MAIL_PASSWORD = "IGLRSEBRHBPKCNOP"
    #默认发送者填写邮箱账号
    MAIL_DEFAULT_SENDER = "17839585182@163.com"

    #redis缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = "6379"

    #设置session过期时间
    PERMANENT_SESSION_LIFTIME = timedelta(days=7)


    #设置分页
    PER_PAGE_COUNT  =10

    #设置图片存储空间
    UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")





class DeveleopmentConfig(BaseConfig):
    #开发环境
    #celery配置
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND ="redis://127.0.0.1:6379/0"

    #个人头像设置
    AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,'avatars')

class TestingConfig(BaseConfig):
    #测试环境
    pass
class ProductionConfig(BaseConfig):
    #生产环境
    pass