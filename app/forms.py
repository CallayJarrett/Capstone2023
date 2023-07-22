from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import BooleanField

class PhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    use_microphone = BooleanField('Use Microphone', default=False)
    audio = FileField('Audio Recording', validators=[
        FileAllowed(['wav', 'flac'], 'Audio files only!')
    ])
     