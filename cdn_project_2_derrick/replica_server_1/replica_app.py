from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)

# Directory for videos on the replica server
VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

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
    try:
        # Attempt to serve the video file
        return send_from_directory(VIDEO_DIR, filename)
    except FileNotFoundError:
        # Handle the case where the video file does not exist
        abort(404, description="Video not found")

if __name__ == '__main__':
    app.run(port=5001)  # Specify the port for the first replica server
