import os
from flask import Blueprint, current_app, flash, g, jsonify, request, url_for,render_template,redirect
from decorators import login_required
from models.post import CommentModel, PostModel,BoardModel
from werkzeug.utils import secure_filename
from exts import csrf
from flask_paginate import Pagination
from exts import db
from forms.post import PublicommentForm
bp =Blueprint("front",__name__,url_prefix="")

@bp.route('/')
def index():
    posts = PostModel.query.all()
    boards = BoardModel.query.all()
    
    
    #获取页码参数
    page = request.args.get("page",type=int,default=1)
    #获取板块参数
    board_id = request.args.get("board_id",type=int,default=0)

    #当前page下的起始位置
    start = (page-1)*current_app.config.get("PER_PAGE_COUNT")
    
    #当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    
    #新增：过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id = board_id)

    #总共有多少帖子
    total =query_obj.count()

    #当前page下的帖子列表
    posts = query_obj.slice(start,end)

    #分页对象
    pagination = Pagination(bs_version =4 ,page=page,total=total,outer_windo=0,inner_window = 2,alignment="center")


    context ={
        "posts":posts,
        "boards":boards,
        "pagination":pagination,
        "current_board":board_id,
    }
    return render_template("front/index.html",**context)




@bp.post("/upload/image")
@csrf.exempt
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

@bp.post("/post/<int:post_id>/comment")
@login_required
def  public_comment(post_id):
    form = PublicommentForm(request.form)
    if form.validate():
        content = form.content.data
        comment = CommentModel(content = content,post_id = post_id,author = g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    
    return redirect(url_for("front.post_detail",post_id=post_id))

