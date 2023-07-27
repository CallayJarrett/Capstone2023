import os
import openai
import pyttsx3
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.speech import *
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import UserForm, LoginForm, PhotoForm
from app.models import User, Photo, VoiceCommand, Designs, ExtendScripts
import speech_recognition as sr

 
@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/edit')
@login_required
def edit():
    # Call the get_uploaded_images function to get a list of filenames
    filenames = get_uploaded_images()

    # Generate a list of image URLs using the url_for function
    image_urls = [url_for('get_image', filename=filename) for filename in filenames]

    # Pass the list of image URLs to the template
    return render_template('edit.html', image_urls=image_urls)

@app.route('/library')
@login_required
def library():
    """Render website's library page."""
    return render_template('library.html')

@app.route('/profile')
@login_required
def profile():
    """Render website's profile page."""
    return render_template('profile.html')

@app.route('/voicecommands')
@login_required
def voicecommands():
    """Render website's upload page."""
    return render_template('voicecommands.html')

@app.route('/designs')
@login_required
def designs():
    """Render website's upload page."""
    return render_template('designs.html')

@app.route('/scripts')
@login_required
def scripts():
    scripts = ExtendScripts.get_all_scripts()
    return render_template('scripts.html', scripts=scripts)

# Set OpenAI API key
openai.api_key = "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"

# Function to transcribe audio
def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print("Unknown error has occurred", e)
        return None

# Function to get OpenAI response
def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    photoform = PhotoForm() 

    if request.method == 'POST':
        if photoform.validate_on_submit():
            photo = request.files['photo']
            audio = request.files['audio']

            if photo and audio:
                filename_photo = secure_filename(photo.filename)
                filename_audio = secure_filename(audio.filename)

                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_photo))
                audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_audio))

                # Transcribe the audio and get the response from OpenAI
                transcribed_text = transcribe_audio(os.path.join(app.config['UPLOAD_FOLDER'], filename_audio))
                if transcribed_text:
                    prompt = "Convert to ExtendScript" + transcribed_text
                    reply = get_openai_response(prompt)
                    print("GPT-3 says:", reply)
                    # Do something with the reply

                return redirect(url_for('upload'))

    return render_template('upload.html', form=photoform)

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
@login_required
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