from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

ENDPOINT = os.environ.get("FACE_ENDPOINT")
API_KEY = os.environ.get("FACE_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    emotion_result = None

    if request.method == "POST":
        image = request.files["image"]

        analyze_url = ENDPOINT + "/face/v1.0/detect"
        params = {'returnFaceAttributes': 'emotion'}

        headers = {
            'Ocp-Apim-Subscription-Key': API_KEY,
            'Content-Type': 'application/octet-stream'
        }

        response = requests.post(
            analyze_url,
            params=params,
            headers=headers,
            data=image.read()
        )

        faces = response.json()

        if faces:
            emotions = faces[0]["faceAttributes"]["emotion"]
            emotion_result = max(emotions, key=emotions.get)
        else:
            emotion_result = "No Face Detected"

    return render_template("index.html", emotion=emotion_result)

if __name__ == "__main__":
    app.run()
