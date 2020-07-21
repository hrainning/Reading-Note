from datetime import datetime
#url_for需要指定蓝本
from flask import render_template, session, redirect, url_for, abort, make_response

from flask import flash,request,current_app

from . import main
from .form import PostForm, EidtProfileForm, EidtProfileAdminForm, CommentForm
from .. import db
from ..decorator import admin_required,permission_required
from ..models import User, Role, Permission, Post, Comment
from flask_login import login_required,current_user

#修饰由蓝本提供，而不是app
@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.is_active  and\
        form.validate_on_submit():
        if current_user.can(Permission.WRITER_ARITICLES):
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    #所有的博客
    posts = pagination.items
    return render_template('index.html',form=form,posts=posts,
                           show_followed=show_followed,pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html',user=user,posts=posts
                           ,pagination=pagination)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EidtProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated')
        return redirect(url_for('.user',username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)


@main.route('/edit-profile/<int:id>',methods=['POST','GET'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EidtProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.account = form.account.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('the profile has been updated')
        return redirect(url_for('.user',username=user.username))
    form.account.data = user.account
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form=form,user=user)

@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form  = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body =form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('your comment has been published')
        return redirect(url_for('.post',id=post.id,page=-1))
    page = request.args.get('page',1,type=int)
    if page == -1:
        page = (post.comments.count() -1)/current_app.config['COMMENT_PER_PAGE'] +1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,per_page=current_app.config['COMMENT_PER_PAGE'],error_out=False)
    comments = pagination.items
    return render_template('post.html',posts=[post],form=form,
    comments=comments,pagiantion=pagination)

@main.route('/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and current_user.is_active:
        if not current_user.can(Permission.ADMINISTER):
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.body = form.body.data
            db.session.add(post)
            flash('the post has been updated')
            return redirect(url_for('.post',id=post.id))
        form.body.data = post.body
        return render_template('edit_post.html',form=form)

@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('you are already following this user')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash('you ar now following %s' %username)
    return redirect(url_for('.user',username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('you are not following this user')
        return redirect(url_for('.user',username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('you are not following %s anvmore' %username)
    return redirect(url_for('.user',username=username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user')
        return redirect('.index')
    page = request.args.get('page',1,type=int)
    pagination = user.followers.paginate(
        page,per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.follower,'timestamp':item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',user=user,title='Followers of',
                           endpoint='.followers',pagination=pagination,
                           follows=follows)

@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followed.paginate(
        page,per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.followed,'timestamp':item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',user=user,title='Followed by',
                           endpoint='.followed_by',pagination=pagination,
                           follows=follows)

@main.route('/all')
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp

@main.route('/moderate')
@login_required
def moderate():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html',comments=comments,
                           pagination=pagination)

@main.route('/moderate/enable/<int:id>')
@login_required
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page', 1, type=int)))

