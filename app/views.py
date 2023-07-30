import os
import openai
import pyttsx3
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.speech import *
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import UserForm, LoginForm, PhotoForm, UploadForm
from app.models import User, Photo, VoiceCommand, Designs, ExtendScripts
import speech_recognition as sr
from app.photo_execute import *


 
@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/edit')
#@login_required
def edit():
    # Call the get_uploaded_images function to get a list of filenames
    filenames = get_uploaded_images()

    # Generate a list of image URLs using the url_for function
    image_urls = [url_for('get_image', filename=filename) for filename in filenames]

    # Pass the list of image URLs to the template
    return render_template('edit.html', image_urls=image_urls)

@app.route('/library')
#@login_required
def library():
    """Render website's library page."""
    return render_template('library.html')

@app.route('/profile')
#@login_required
def profile():
    """Render website's profile page."""
    return render_template('profile.html')

@app.route('/voicecommands')
#@login_required
def voicecommands():
    """Render website's upload page."""
    return render_template('voicecommands.html')

@app.route('/designs')
#@login_required
def designs():
    """Render website's upload page."""
    return render_template('designs.html')

@app.route('/scripts')
#@login_required
def scripts():
    scripts = ExtendScripts.get_all_scripts()
    return render_template('scripts.html', scripts=scripts)

"""@app.route('/shortcuts', methods=['GET', 'POST'])
def shortcuts():
    
    if request.method == 'POST':
        photo = request.files['file']
        script_filename = request.form.get('script')

        if photo and script_filename:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            script_file_path = os.path.join(app.config['SCRIPTS_FOLDER'], script_filename)

            # Call the function to open Photoshop with the uploaded photo
            open_photoshop_cs6(photo_path)

            # Call the function to execute the selected script file
            execute_script(script_file_path)

            # Flash message or any other response you want to return to the user
            flash('File uploaded and script executed successfully.')

            return jsonify({"success": True}), 200

    
    uploadform = UploadForm()
    return render_template('shortcuts.html', uploadform = uploadform) """



@app.route('/shortcuts', methods=['GET', 'POST'])
def shortcuts():
    """Render website's shortcut edits page."""
    if request.method == 'POST':
        photo = request.files['file']
        script_filename = request.form.get('script')

        if photo and script_filename:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            script_file_path = os.path.join(app.config['SCRIPTS_FOLDER'], script_filename)

            # Call the function to open Photoshop with the uploaded photo
            open_photoshop_cs6(photo_path)

            # Call the function to execute the selected script file
            execute_script(script_file_path)

            # Flash message or any other response you want to return to the user
            flash('File uploaded and script executed successfully.')

            return jsonify({"success": True}), 200

    uploadform = UploadForm()
    return render_template('shortcuts.html', uploadform=uploadform)


# Set OpenAI API key
openai.api_key = "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"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to transcribe audio
def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        ar = recognizer.record(source)
    try:
        text = recognizer.recognize_google(ar)
        print("text:")
        print(text)
    except Exception as e:
            print("Unknown error has occurred", e)
    return text

# Function to get OpenAI response
# def get_openai_response(prompt):
#     try:
#         reply = get_openai_response("Convert to ExtendScript"+text)
#         print("GPT-3 says:", reply)
#         #return redirect(url_for("loading",photo=filename, text=text, reply=reply))
#     except Exception as e:
#         print("Unknown error has occurred", e)
#     return reply

def convert_to_text(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        ar = recognizer.record(source)
    try:
        text = recognizer.recognize_google(ar)
        print("text:")
        print(text)
    except Exception as e:
            print("Unknown error has occurred", e)
    return text

def generate_extendscript(text):
    try:
        reply = get_openai_response("Convert to ExtendScript"+text)
        print("GPT-3 says:", reply)
        #return redirect(url_for("loading",photo=filename, text=text, reply=reply))
    except Exception as e:
        print("Unknown error has occurred", e)
    return reply

@app.route('/upload', methods=['POST', 'GET'])
#@login_required
def upload():
    photoform = PhotoForm()
    
    
    if photoform.validate_on_submit():
        
        photo = photoform.photo.data # we could also use request.files['photo']
        audio = photoform.audio.data      

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
    
          
        filenameAudio = secure_filename(audio.filename)
        print(filenameAudio)
        #audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filenameAudio))
        text = convert_to_text(audio)
        print("this,",text)

        reply = generate_extendscript(text)
        print(reply)
        #return redirect(url_for("loading",photo=filename, text=text, reply=reply))

    return render_template('upload.html', form=photoform)

# # Route to handle user speech input from microphone
# @app.route('/process_microphone', methods=['POST'])
# def process_microphone():
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         text = recognizer.recognize_google(audio)
#         print("You said:", text)
#         reply = get_openai_response(text)
#         print("GPT-3 says:", reply)
#         speak_response(reply)
#         return reply
#     except sr.UnknownValueError:
#         return "Speech recognition could not understand audio. Please try again."
#     except sr.RequestError as e:
#         return "ERROR: {0}".format(e)

# # Route to handle user speech input from uploaded file
# @app.route('/process_file', methods=['POST'])
# def process_file():
#     audio_file = request.files['audio']
#     audio_file.save('uploaded_audio.wav')

#     try:
#         text = transcribe_audio('uploaded_audio.wav')
#         print("Transcribed text:", text)
#         reply = get_openai_response(text)
#         print("Response:", reply)
#         speak_response(reply)
#         return reply
#     except Exception as e:
#         return "An error occurred: {0}".format(e)
    
def get_uploaded_images():
    upload_dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    filenames = []
    for filename in os.listdir(upload_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            filenames.append(filename)
    return filenames

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/command')
def command():
    """Render website's command page."""
    return render_template('command.html')

@app.route('/commit')
def commit():
    """Render website's commit page."""
    return render_template('commit.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    userform = UserForm()

    if request.method == 'POST':
        # Get the form data submitted by the user
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        profile_photo = request.files.get('profile_photo')

        # Validate file upload on submit
        if not username or not password or not firstname or not lastname:
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))

        if profile_photo and allowed_file(profile_photo.filename):
            filename = secure_filename(profile_photo.filename)

            # Check the length of the filename
            if len(filename) > 100:
                flash('Profile photo filename is too long', 'danger')
                return redirect(url_for('register'))

            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid file format for profile photo', 'danger')
            return redirect(url_for('register'))

        # Check if username already exists in the database
        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        # Create and save the new user to the database
        user = User(username=username, password=password, firstname=firstname, lastname=lastname,
                    profile_photo=filename)
        db.session.add(user)
        db.session.commit()

        flash('User added successfully!', 'success')
        return redirect(url_for('login'))

    # If the request method is GET, render the registration page
    return render_template('register.html', form=userform)

def allowed_file(filename):
    # Add more allowed file extensions if needed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            # flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)