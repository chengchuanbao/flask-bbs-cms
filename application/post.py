import os
from flask import Blueprint, current_app, g, jsonify,request,render_template, url_for
from models.post import BoardModel, PostModel
from decorators import login_required
from exts import csrf,db
from werkzeug.utils import secure_filename
from forms.post import PublicPostForm
from utils import restful
bp = Blueprint("post",__name__,url_prefix='')


 
@bp.route("post/public",methods = ["GET","POST"])
@login_required
def public_post():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/public_post.html",boards = boards)
    else:
        form =PublicPostForm(request.form)
        if  form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title = title,content = content ,board_id=board_id,author = g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok
        else:
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.post("/upload/image")
@csrf.exempt
@login_required
def upload_image():
    f = request.files.get('image')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg','gif','png','jpeg']:
        return jsonify({
            "errorno":400,
            "data":[]
            
        })
    filename = secure_filename(f.filename)
    f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"),filename))
    url = url_for("media.media_file",filename = filename)
    return jsonify({
        "errorno":0,
        "data":[{
            "url":url,
            "alt":"",
            "href":""
        }]
    })


###动态加载帖子详情数据
@bp.get("/post/detail<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count+=1
    db.session.commit()
    return render_template("front/post_detail.html",post=post)


