from flask import  render_template,redirect,request,url_for,flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .form import LoginForm,RegistrationForm,ChangePasswordForm,PasswordResetForm,PasswordResetFormRequest,ChangeUsernameForm
from .. import db

#requets前的操作钩子
@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed\
        and request.endpoint[:5] != 'auth.'\
        and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            #用户访问未授权的 URL 时会显示登录表单，Flask-Login
            #会把原地址保存在查询字符串的 next 参数中，这个参数可从 request.args 字典中读取。
            #如果查询字符串中没有 next 参数，则重定向到首页。
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(account=form.account.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('your password has been updated.')
            return redirect(url_for('main.index'))
        else :
            flash('Invalid password')
    return render_template("auth/change_password.html",form=form)

@auth.route('/change-username',methods=['POST','GET'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('your name has been updated')
        return redirect(url_for('main.index'))
    return render_template('auth/change_username.html',form=form)

@auth.route('/reset',methods=['POST','GET'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetFormRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        if user:
            if user.username == form.username.data:
                return redirect(url_for('auth.password_reset',account=user.account))
            else:
                flash('you are bad boy!')
        else:
            flash('The account not register!')
    return render_template("auth/reset_password.html",form=form)

@auth.route('/reset/<account>',methods=['POST','GET'])
def password_reset(account):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=account).first()
        if user:
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash('your password has been update.')
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)