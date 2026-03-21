from flask import Flask, render_template, request, send_file, session, redirect, url_for
import os
import subprocess
import zipfile
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
'''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio')
def audio():
    return render_template('audio.html')
'''
@app.route('/')
def video():
    return render_template('video.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    if not file or file.filename == "":
        return "No file uploaded."

    image = request.files.get('image')
    conversion_type = request.form.get('type')
    output_format = request.form.get('format', 'mp4')
    
    # Get session ID for multiple files
    session_id = request.form.get('session_id', str(uuid.uuid4()))
    session['session_id'] = session_id
    
    # Create session folders
    session_upload = os.path.join(UPLOAD_FOLDER, session_id)
    session_output = os.path.join(OUTPUT_FOLDER, session_id)
    os.makedirs(session_upload, exist_ok=True)
    os.makedirs(session_output, exist_ok=True)

    filename = secure_filename(file.filename)
    input_path = os.path.join(session_upload, filename)
    file.save(input_path)

    # Generate unique output filename
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_converted.{output_format}"
    output_path = os.path.join(session_output, output_filename)

    if conversion_type == "audio_to_video":
        color = request.form.get("color", "black")
        if image and image.filename != "":
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(session_upload, image_filename)
            image.save(image_path)

            command = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", image_path,
                "-i", input_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
        else:
            command = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c={color}:s=1280x720",
                "-i", input_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]

    elif conversion_type == "video_to_audio":
        command = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-q:a", "0",
            "-map", "a",
            output_path
        ]
    else:
        return "Invalid conversion type."

    result = subprocess.run(command, capture_output=True, text=True)

    if not os.path.exists(output_path):
        return f"Error:\n{result.stderr}"

    # Store converted file info in session
    if 'converted_files' not in session:
        session['converted_files'] = []
    session['converted_files'].append(output_filename)
    session.modified = True

    return render_template('result.html', 
                         filename=output_filename, 
                         session_id=session_id,
                         conversion_type=conversion_type)

@app.route('/download/<session_id>/<filename>')
def download(session_id, filename):
    file_path = os.path.join(OUTPUT_FOLDER, session_id, filename)
    return send_file(file_path, as_attachment=True)

@app.route('/download_all/<session_id>')
def download_all(session_id):
    session_folder = os.path.join(OUTPUT_FOLDER, session_id)
    zip_path = os.path.join(OUTPUT_FOLDER, f"{session_id}_all.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(session_folder):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    
    return send_file(zip_path, as_attachment=True)

@app.route('/clear_session/<session_id>')
def clear_session(session_id):
    # Clear session files
    session_upload = os.path.join(UPLOAD_FOLDER, session_id)
    session_output = os.path.join(OUTPUT_FOLDER, session_id)
    
    import shutil
    if os.path.exists(session_upload):
        shutil.rmtree(session_upload)
    if os.path.exists(session_output):
        shutil.rmtree(session_output)
    
    session.pop('converted_files', None)
    session.pop('session_id', None)
    
    return redirect(url_for('video'))

if __name__ == "__main__":
    app.run(debug=True)