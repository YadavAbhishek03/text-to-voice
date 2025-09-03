from flask import Flask, render_template, request
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            return "⚠️ No text provided!"

        image_file = request.files.get("image")
        if not image_file:
            return "⚠️ No image uploaded!"

        # Save image
        image_path = os.path.join("static", "uploaded_image.jpg")
        image_file.save(image_path)

        # Text -> Speech
        audio_path = os.path.join("static", "output.mp3")
        tts = gTTS(text)
        tts.save(audio_path)

        # Image + Audio -> Video
        audio = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(audio.duration)
        image_clip = image_clip.set_audio(audio)
        video_path = os.path.join("static", "output.mp4")
        image_clip.write_videofile(video_path, fps=24)

        return render_template("result.html", video_file="output.mp4")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
