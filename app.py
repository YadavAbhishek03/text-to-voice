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
def welcome():
    return render_template('welcome.html')


@app.route('/text-to-voice', methods=['GET', 'POST'])
def text_to_voice():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            tts = gTTS(text)
            audio_filename = f"{uuid.uuid4()}_text.mp3"
            audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
            tts.save(audio_path)
            return render_template("result.html", audio_file=f"results/{audio_filename}")
    return render_template('text_to_voice.html')


@app.route('/text-image-video', methods=['GET', 'POST'])
def text_image_video():
    if request.method == 'POST':
        text = request.form.get('text')
        image = request.files.get('image')

        if text and image:
            # text → audio
            tts = gTTS(text)
            text_audio_path = os.path.join(OUTPUT_FOLDER, "text_audio.mp3")
            tts.save(text_audio_path)
            text_audio = AudioFileClip(text_audio_path)

            # image save
            image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{image.filename}")
            image.save(image_path)

            # video
            video_filename = f"{uuid.uuid4()}_output.mp4"
            video_path = os.path.join(OUTPUT_FOLDER, video_filename)
            image_clip = ImageClip(image_path).set_duration(text_audio.duration).set_audio(text_audio)
            image_clip.write_videofile(video_path, fps=24)

            return render_template("result.html", video_file=video_filename)
    return render_template('text_image_video.html')


@app.route('/audio-image-video', methods=['GET', 'POST'])
def audio_image_video():
    if request.method == 'POST':
        audio = request.files.get('audio')
        image = request.files.get('image')

        if audio and image:
            # save audio
            audio_filename = f"{uuid.uuid4()}_audio.mp3"
            audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
            audio.save(audio_path)
            user_audio = AudioFileClip(audio_path)

            # save image
            image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{image.filename}")
            image.save(image_path)

            # video
            video_filename = f"{uuid.uuid4()}_output.mp4"
            video_path = os.path.join(OUTPUT_FOLDER, video_filename)
            image_clip = ImageClip(image_path).set_duration(user_audio.duration).set_audio(user_audio)
            image_clip.write_videofile(video_path, fps=24)

            return render_template("result.html", video_file=video_filename)
    return render_template('audio_image_video.html')


@app.route('/text-audio-image-video', methods=['GET', 'POST'])
def text_audio_image_video():
    if request.method == 'POST':
        text = request.form.get('text')
        audio = request.files.get('audio')
        image = request.files.get('image')

        text_audio = None
        user_audio = None

        if text:
            tts = gTTS(text)
            text_audio_path = os.path.join(OUTPUT_FOLDER, "text_audio.mp3")
            tts.save(text_audio_path)
            text_audio = AudioFileClip(text_audio_path)

        if audio and audio.filename != "":
            audio_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}_uploaded.mp3")
            audio.save(audio_path)
            user_audio = AudioFileClip(audio_path)

        final_audio = None
        if text_audio and user_audio:
            final_audio = CompositeAudioClip([text_audio, user_audio])
        elif text_audio:
            final_audio = text_audio
        elif user_audio:
            final_audio = user_audio

        if image and final_audio:
            image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{image.filename}")
            image.save(image_path)

            video_filename = f"{uuid.uuid4()}_output.mp4"
            video_path = os.path.join(OUTPUT_FOLDER, video_filename)

            image_clip = ImageClip(image_path).set_duration(final_audio.duration).set_audio(final_audio)
            image_clip.write_videofile(video_path, fps=24)

            return render_template("result.html", video_file=video_filename)

    return render_template('text_audio_image_video.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)

