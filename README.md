
# Facial Recognition for Mood Detection using Microsoft Azure

Project Overview:
This project implements live facial mood detection using Microsoft Azure AI Face service.
The system captures an image from a webcam, sends it to Azure Face API, and receives 
emotion detection results in real time.

Cloud Platform Used:
- Microsoft Azure
- Azure AI Face (Cognitive Service)
- Azure App Service (Web Hosting)

Objective:
To demonstrate cloud-based AI integration, REST API usage, and PaaS deployment 
for real-time facial emotion detection.

## PHASE 1 – Azure Cloud Setup

### Step 1: Create Azure AI Face Resource

1. Login to https://portal.azure.com
2. Click on “Create a Resource”.
3. Search for “Face”.
4. Select Azure AI Face and click Create.
5. Choose:
   - Subscription: Student subscription
   - Resource Group: Create new (example: mood-rg)
   - Region: Closest region (e.g., Central India)
   - Pricing Tier: F0 (Free Tier)
6. Click Review + Create → Create.

After deployment:
- Go to Resource → Keys and Endpoint.
- Copy Key and Endpoint for later use.


### Step 2: Create Azure App Service (Web Hosting)

1. Click Create Resource.
2. Select Web App.
3. Choose:
   - Resource Group: mood-rg
   - Runtime Stack: Python 3.9
   - Pricing Plan: F1 (Free Tier)
4. Click Create.

This will host the Flask web application in the cloud.

## PHASE 2 – Local Project Development

### Step 3: Install Requirements

Install Python 3.9 or above.
Open Command Prompt and verify:
python --version

Install required libraries:
pip install flask requests

Create project folder structure:

    mood_app/
    ├── app.py
    ├── requirements.txt
    └── templates/
            └── index.html
### Step 4: Create requirements.txt

Add the following: (It given in mood_rg file)

    flask
    requests
    gunicorn

This file is required for Azure deployment.

### Step 5: Flask Application Code (app.py)

Paste the following code into app.py: (It given in mood_rg file)

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


### Step 6: HTML Live Camera Code (templates/index.html)

paste the following code into index.html: (It given in mood_rg file)

    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Mood Detection</title>
    </head>
    <body>

    <h1>Live Facial Mood Detection</h1>

    <video id="video" width="400" autoplay></video>
    <br><br>
    <button onclick="capture()">Detect Emotion</button>

    <h2 id="result"></h2>

    <script>
    const video = document.getElementById('video');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        });

    function capture() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob);

            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                document.getElementById("result").innerText = data;
            });
        }, 'image/jpeg');
    }
    </script>

    </body>
    </html>


## PHASE 3 – Azure Deployment

### Step 7: Configure Environment Variables

In Azure Portal:
1. Go to Web App.
2. Click Configuration → Application Settings.
3. Add:
   - FACE_ENDPOINT = your endpoint
   - FACE_KEY = your API key
4. Save and Restart Web App.

### Step 8: Deploy Application

1. Zip the following files:
   - app.py
   - requirements.txt
   - templates folder
2. Go to Web App → Deployment Center.
3. Choose ZIP Deploy.
4. Upload the ZIP file.
5. Restart Web App.

Open the Web App URL and allow camera access.

## Architecture Explanation:

User Webcam → Flask Web App → Azure App Service → Azure Face API → 
Emotion Detection JSON → Display Result

### Cloud Model Used:
- PaaS (Platform as a Service)
- REST API Integration
- Serverless AI Model (Pre-trained Azure Service)

### Advantages:
- No need to train ML model
- Scalable cloud architecture
- Secure key management
- Cost-effective (Free tier usage)

### Cost Management Strategy

- Use F0 Free Tier for Face API.
- Use F1 Free Tier for App Service.
- Stop or delete resource group after demonstration.
- Monitor credits in Azure Cost Management dashboard.

### Conclusion

This project demonstrates real-time facial mood detection using cloud-based AI services.
It integrates web technologies with Microsoft Azure AI and follows cloud computing 
best practices including scalability, security, and cost optimization.


