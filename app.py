from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Configuration for file uploads
STL_FILES = 'STL_FILES'
app.config['STL_FILES'] = STL_FILES

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "stl"

@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    # Get the button value
    buttonval = request.form.get('submit')

    if file.filename == '':
        return 'No selected file'

    if buttonval == 'rapid':
        configfile = 'fast.ini'
    elif buttonval == 'hi-res':
        configfile = 'slow.ini'
    if buttonval == 'rapid-support':
        configfile = 'fastSupport.ini'
    elif buttonval == 'hi-res-support':
        configfile = 'slowSupport.ini'


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['STL_FILES'], filename))
        return f'Starting {filename}, with {buttonval} preset.'
    else:
        return 'Invalid file type'



if __name__ == '__main__':
    app.run(debug=True, port=3000)

    stlfile = ''


    class SimpleHandler(FileSystemEventHandler):
        def on_created(self, event):
            global stlfile
            global configfile
            global filename
            stlfile = event.src_path
            command = [
                "prusa-slicer",
                "--load", f"configs/"+configfile,
                "--slice", filename,
                "--output", stlfile+".gcode"
            ]
            result = subprocess.run(command, capture_output=True, text=True)

            # Print the output and errors (if any)
            print("STDOUT:")
            print(result.stdout)

            print("STDERR:")
            print(result.stderr)

            # Check the return code to ensure the command ran successfully
            if result.returncode == 0:
                print("Slicing completed successfully!")
            else:
                print(f"Error occurred! Return code: {result.returncode}")


    folder = "STL_FILES"

    event_handler = SimpleHandler()
    observer = Observer()

    observer.schedule(event_handler, folder)

    observer.start()

    try:
        print(f"Watching folder: {folder}")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
