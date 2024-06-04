

import time
import threading
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session
import main, nutrient_info

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysupersecretkey"
app.config["SESSION_TYPE"] = "filesystem"

server_session = Session(app)

UPLOAD_FOLDER = './input'
INPUT_FOLDER = './input'

# Global dictionary to store session data
session_data = {}

def slow_loading_function(image_path, output_path, session_id):
    """Simulates a time-consuming process"""
    volumes = main._main(image_path, output_path)
    info = {}
    total = {}

    total, info = main.calc_total(volumes)

    session_data[session_id] = {"info": info, "total": total}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading', methods=['POST'])
def loading():
    if request.method == 'POST':
        image_file = request.files['image-upload']
        if image_file:
            filename = image_file.filename
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            name, ext = filename.split('.')
            if ext in allowed_extensions:
                image_path = f'{UPLOAD_FOLDER}/test.jpg'
                output_path = f'{INPUT_FOLDER}/test.json'
                image_file.save(image_path)
                
                session_id = request.cookies.get("session")  # Use request.cookies.get("session") instead of request.sid

                session["session_id"] = session_id

                # Start the background thread
                thread = threading.Thread(target=slow_loading_function, args=(image_path, output_path, session_id))
                thread.start()

                return render_template("loading.html")
            else:
                session["message"] = 'Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF'
                return redirect(url_for('index'))
        else:
            session["message"] = 'No image file selected.'
            return redirect(url_for('index'))



@app.route('/results')
def results():
    session_id = session.get("session_id")
    data = session_data.get(session_id, {})
    info = data.get("info")
    total = data.get("total")
    message = session.get("message", "")

    return render_template('results.html', info=info, total=total, message=message)


@app.route("/check_status")
def check_status():
    session_id = session.get("session_id")
    if session_id in session_data:
        return jsonify({"status": "done"})
    else:
        return jsonify({"status": "processing"})


if __name__ == '__main__':
    app.run(debug=True)


