"""
用来存放第三方插件的对象
"""
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_avatars import Avatars


csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
cache = Cache()
avatras = Avatars()