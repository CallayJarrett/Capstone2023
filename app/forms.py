from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UserForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = StringField('Password', [validators.InputRequired()])
    firstname = StringField('First Name', [validators.InputRequired()])
    lastname = StringField('Last Name', [validators.InputRequired()])

    profile_photo = FileField('Profile Photo', validators=[
                FileRequired(),
                FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')
            ]
    )

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

class PhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])