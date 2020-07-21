from flask_wtf import FlaskForm
from  wtforms import StringField,PasswordField,BooleanField,SubmitField
from  wtforms.validators import Required,Length,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    account = StringField('Account',validators=[Required(),Length(1,32)])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('keep me logged in ')
    submit = SubmitField('LogIN')


class RegistrationForm(FlaskForm):
    account = StringField('Account', validators=[Required(), Length(1, 32)])
    username = StringField('Username',validators=[
        Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                       'username must have only letters,'
                                       'numbers,dots or inderscores')
    ])
    password = PasswordField('Password', validators=[
        Required(),EqualTo('password2',message='passwords must match.')])
    password2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Register')

    #validate_开头的函数 均自动调用
    def validate_account(self,field):
        if User.query.filter_by(account=field.data).first():
            raise ValidationError('Account already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password',validators=[Required()])
    password = PasswordField('New password',validators=[
        Required(),EqualTo('password2',message='passwords must match.')
    ])
    password2 = PasswordField('Confirm new password',validators=[Required()])
    submit = SubmitField('Update Password')

class ChangeUsernameForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'username must have only letters,'
                                          'numbers,dots or inderscores')
    ])
    submit = SubmitField('Update username')

class PasswordResetFormRequest(FlaskForm):
    account = StringField('Account', validators=[Required(), Length(1, 32)])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'username must have only letters,'
                                          'numbers,dots or inderscores')
    ])
    submit = SubmitField('Check username')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',validators=[
        Required(),EqualTo('password2',message='password must match')
    ])
    password2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Reset Password')