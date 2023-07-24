import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.speech import *
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import UserForm, LoginForm, PhotoForm
from app.models import User, Photo, VoiceCommand, Designs, ExtendScriptFile
import speech_recognition as sr


 
@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/edit')
def edit():
    # Call the get_uploaded_images function to get a list of filenames
    filenames = get_uploaded_images()

    # Generate a list of image URLs using the url_for function
    image_urls = [url_for('get_image', filename=filename) for filename in filenames]

    # Pass the list of image URLs to the template
    return render_template('edit.html', image_urls=image_urls)

@app.route('/library')
def library():
    """Render website's library page."""
    return render_template('library.html')

@app.route('/profile')
def profile():
    """Render website's profile page."""
    return render_template('profile.html')

@app.route('/voicecommands')
def voicecommands():
    """Render website's upload page."""
    return render_template('voicecommands.html')

@app.route('/designs')
def designs():
    """Render website's upload page."""
    return render_template('designs.html')

@app.route('/scripts')
def scripts():
    """Render website's upload page."""
    return render_template('scripts.html')

@app.route('/upload',methods=['POST','GET'])
def upload():
    """Render website's upload page."""
    photoform = PhotoForm()
    recognizer = sr.Recognizer()
    
    if photoform.validate_on_submit():
        
        photo = photoform.photo.data 
        audio = photoform.audio.data      

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
    
          
        filenameAudio = secure_filename(audio.filename)
        print(filenameAudio)
        #audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filenameAudio))
        
        
        with sr.AudioFile(audio) as source:
            ar = recognizer.record(source)
        try:
            text = recognizer.recognize_google(ar)
            print("text:")
            print(text)
            reply = get_openai_response("Convert to ExtendScript"+text)
            print("GPT-3 says:", reply)
        except Exception as e:
            print("Unknown error has occurred", e)
         

    return render_template('upload.html',form=photoform)

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

# # Route to handle user speech input from microphone
# @app.route('/process_microphone', methods=['POST'])
# def process_microphone():

#     audio_data = request.files['audio_data'] 
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         text = recognizer.recognize_google(audio)
#         print("You said:", text)
#        # reply = get_openai_response(text)
#         ##print("GPT-3 says:", reply)
#         #speak_response(reply)
#         return text
#     except sr.UnknownValueError:
#         return "Speech recognition could not understand audio. Please try again."
#     except sr.RequestError as e:
#         return "ERROR: {0}".format(e)

# # Route to handle user speech input from uploaded file
# @app.route('/process_file', methods=['POST'])
# def process_file():
#     # audio_file = request.files['audio']
#     # audio_file.save('uploaded_audio.wav')

#     # try:
#     #     text = transcribe_audio('uploaded_audio.wav')
#     #     print("Transcribed text:", text)
#     #     reply = get_openai_response(text)
#     #     print("GPT-3 says:", reply)
#     #     speak_response(reply)
#     #     return reply
#     # except Exception as e:
#     #     return "An error occurred: {0}".format(e)
#     filename = request.args.get('photo','')
#     text = request.args.get('text','')
#     reply = request.args.get('reply','')
#     status_message = f"Process complete.<br>Photo: {filename}<br>You Said: {text}<br>ExtendScript: {reply}"

#     return render_template('loading.html', status=status_message)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)