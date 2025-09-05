from flask import Flask, render_template, request
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    image = request.files.get('image')
    audio = request.files.get('audio')

    text_audio = None
    user_audio = None

    # Case 1: Text -> gTTS audio
    if text:
        tts = gTTS(text)
        text_audio_path = os.path.join(OUTPUT_FOLDER, "text_audio.mp3")
        tts.save(text_audio_path)
        text_audio = AudioFileClip(text_audio_path)

    # Case 2: User uploaded audio
    if audio and audio.filename != "":
        audio_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}_uploaded.mp3")
        audio.save(audio_path)
        user_audio = AudioFileClip(audio_path)

    # Mix audio if both are present
    final_audio = None
    if text_audio and user_audio:
        final_audio = CompositeAudioClip([text_audio, user_audio])
    elif text_audio:
        final_audio = text_audio
    elif user_audio:
        final_audio = user_audio

    video_file = None
    audio_file = None

    # Case A: If image + some audio available → make video
    if image and image.filename != "" and final_audio:
        image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{image.filename}")
        image.save(image_path)

        video_filename = f"{uuid.uuid4()}_output.mp4"
        video_path = os.path.join(OUTPUT_FOLDER, video_filename)

        image_clip = ImageClip(image_path).set_duration(final_audio.duration)
        image_clip = image_clip.set_audio(final_audio)
        image_clip.write_videofile(video_path, fps=24)

        video_file = video_filename

    # Case B: If only audio generated
    elif final_audio:
        audio_filename = f"{uuid.uuid4()}_output.mp3"
        audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
        final_audio.write_audiofile(audio_path)
        audio_file = f"results/{audio_filename}"

    return render_template("result.html", video_file=video_file, audio_file=audio_file)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
