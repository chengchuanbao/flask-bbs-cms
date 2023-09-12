from flask import Flask 
import config
from exts import db,mail,cache
from flask_migrate import Migrate
from models import user
import command
from exts import csrf,avatras
from bbs_celery import make_celery
import hooks
import filters
import logging






app = Flask(__name__)

app.config.from_object(config.DeveleopmentConfig)
app.before_request(hooks.bbs_before_request)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatras.init_app(app)
# 设置日志级别
app.logger.setLevel(logging.INFO)


#构建celery
celery = make_celery(app)


migrate = Migrate(app,db)

#添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)

#添加命令
app.cli.command("create-permission")(command.create_permission)
app.cli.command("create-role")(command.create_role)
app.cli.command("create-test-user")(command.create_test_user)
app.cli.command("create-admin")(command.create_admin)
app.cli.command("create-board")(command.create_board)
app.cli.command("create-test-post")(command.create_test_post)

app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)





from application.front import bp as front_bp
app.register_blueprint(front_bp)
from application.cms import bp as cms_bp
app.register_blueprint(cms_bp)

from application.user import bp as user_bp
app.register_blueprint(user_bp)
from application.post import bp as post_bp
app.register_blueprint(post_bp)

from application.media import bp as media_bp
app.register_blueprint(media_bp)


if __name__ =="__main__":
    app.run(debug = True)