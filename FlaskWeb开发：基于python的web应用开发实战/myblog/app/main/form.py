from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Regexp, ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

from flask_login import current_user

#定义表单
class NameForm(FlaskForm):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

class EidtProfileForm(FlaskForm):
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EidtProfileAdminForm(FlaskForm):

    account = StringField('Account',validators=[Length(0, 64)])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EidtProfileAdminForm, self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_account(self, field):
        if current_user.account != field.data:
            if User.query.filter_by(account=field.data).first():
                raise ValidationError('Account already registered.')

    def validate_username(self,field):
        if field.data != self.user.username and\
            User.query.filter_by(username=field.data).first():
            raise ValidationError('Uername already in use.')

class PostForm(FlaskForm):
    body = PageDownField("what's on your mind?",validators=[Required()])
    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    body  = StringField('',validators=[Required()])
    submit = SubmitField('Submit')
