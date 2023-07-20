from . import db
from werkzeug.security import generate_password_hash

# User model to store login credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    profile_photo = db.Column(db.String)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  
        except NameError:
            return str(self.id)
    
    def __init__(self, username, password, firstname, lastname, profile_photo):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.profile_photo = profile_photo

    def __repr__(self):
        return f'<User %r {self.id}>'

# Photo model to store uploaded photos
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

    def __init__(self, id, user_id, file_path):
        self.id = id
        self.user_id = user_id
        self.file_path = file_path
    
    def __repr__(self):
        return f'<Photo %r {self.id}>'

# Voice command model
class VoiceCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    command_prompt = db.Column(db.String(200), nullable=False)

    def __init__(self, id, user_id, command_prompt):
        self.id = id
        self.user_id = user_id
        self.command_prompt = command_prompt
    
    def __repr__(self):
        return f'<VoiceCommand %r {self.id}>'

# Edited design model
class Designs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    design_file_path = db.Column(db.String(200), nullable=False)

    def __init__(self, id, user_id, design_file_path):
        self.id = id
        self.user_id = user_id
        self.design_file_path = design_file_path
    
    def __repr__(self):
        return f'<Designs %r {self.id}>'

# ExtendScript file model
class ExtendScriptFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    script_file_path = db.Column(db.String(200), nullable=False)

    def __init__(self, id, user_id, script_file_path):
        self.id = id
        self.user_id = user_id
        self.script_file_path = script_file_path
    
    def __repr__(self):
        return f'<ExtendScriptFile %r {self.id}>'
