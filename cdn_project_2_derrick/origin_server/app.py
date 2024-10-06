from flask import Flask, request, send_file
import os

app = Flask(__name__)

# Set the video directory path
VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

# Ensure the videos directory exists
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

@app.route('/')
def index():
    return "Origin Server is running."

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video file provided.", 400

    video_file = request.files['video']
    video_path = os.path.join(VIDEO_DIR, video_file.filename)
    video_file.save(video_path)

    return f"Video '{video_file.filename}' uploaded successfully.", 201

@app.route('/video/<filename>', methods=['GET'])
def get_video(filename):
    video_path = os.path.join(VIDEO_DIR, filename)
    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=False)
    else:
        return "Video not found.", 404

if __name__ == "__main__":
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    app.run(host='0.0.0.0', port=5000)
