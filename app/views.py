import os
from app import app
from flask import render_template, request, redirect, url_for, flash
from app.speech import *
from werkzeug.utils import secure_filename
from app.forms import PhotoForm


@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/edit')
def edit():
    """Render website's edit page."""
    return render_template('edit.html')

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


@app.route('/uploadphoto')
def uploadphoto():
    """Render website's upload page."""
    photoform = PhotoForm()

    if photoform.validate_on_submit():

        photo = photoform.photo.data # we could also use request.files['photo']
       

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

    return render_template('upload.html', filename=filename, form=photoform)

   

@app.route('/command')
def command():
    """Render website's command page."""
    return render_template('command.html')

@app.route('/commit')
def commit():
    """Render website's commit page."""
    return render_template('commit.html')

# Route to handle user speech input from microphone
@app.route('/process_microphone', methods=['POST'])
def process_microphone():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        reply = get_openai_response(text)
        print("GPT-3 says:", reply)
        speak_response(reply)
        return reply
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio. Please try again."
    except sr.RequestError as e:
        return "ERROR: {0}".format(e)

# Route to handle user speech input from uploaded file
@app.route('/process_file', methods=['POST'])
def process_file():
    audio_file = request.files['audio']
    audio_file.save('uploaded_audio.wav')

    try:
        text = transcribe_audio('uploaded_audio.wav')
        print("Transcribed text:", text)
        reply = get_openai_response(text)
        print("GPT-3 says:", reply)
        speak_response(reply)
        return reply
    except Exception as e:
        return "An error occurred: {0}".format(e)


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

   
