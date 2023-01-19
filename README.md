# Roboflow Model Tester

This App allows you to use models from the [Roboflow Vision AI platform](https://roboflow.com/) on your camera Swarm. The Roboflow platform has a library with a lot of readily trained models provided by the community in the [Roboflow Universe](https://universe.roboflow.com/).

<img src="https://storage.googleapis.com/reswarm-images/Roboflow_universe.png" width="600px;" style="margin-bottom: 24px;">

You can use any of the provided models by providing the following parameters at the installed app:

Parameter | Description
--- | ---
Roboflow API Key | The API for your account on the Roboflow Platform
Project Name | The project identifier to use. The project must have an existing trained model.
Model Version | The version of the model to use for inference.

On an installed app you enter these parameters in the paramter menu:

<div style="display: flex; align-items: start; justify-content: space-around;">
    <img src="https://storage.googleapis.com/reswarm-images/Roboflow_screen1.png" width="300px"/>
    <img src="https://storage.googleapis.com/reswarm-images/Roboflow_screen2.png" width="300px"/>
</div>

# Using your own Camera Device Hardware

To use the Roboflow Test app on your own edge PC hardware with an attached camera, you need to register your edge PC in a Swarm in the Record Evolution edge platform.

Just a few steps are required depending on the kind of device you are using.
Please take a look at our documentation [here](https://docs.record-evolution.de/#/en/Reswarm/connect-devices).


# Inspecting the Video Output

To get a live view of each of the cameras in your swarm you need to enable the remote access feature on the cameras.

You do this in the settings of the installed app. 
Once the remote access is enabled a little globe badge is added to the app icon. Now just click the app icon and the video feed opens in a new browser window.

<div style="display: flex; align-items: start; justify-content: space-around;">
    <img src="https://storage.googleapis.com/reswarm-images/Roboflow_settings.png" width="300px"/>
    <img src="https://storage.googleapis.com/reswarm-images/Roboflow_public_badge.png" width="300px"/>
    <img src="https://storage.googleapis.com/reswarm-images/Roboflow_plants_video.png" width="300px"/>
</div>


# Data Collection

The models provide the detection results as a json file that can be sent to a Data Pod within the platform.

To publish data, this app uses the integrated WAMP message broker and uses the topic given by you in the paramters of the App:

Parameter | Description
--- | ---
Publish Topic | The topic under which subscribers in a Data Pod can receive the data.

Note that the image itself is not part of the message payload.

To receive the json data in a Data Pod you need to 

1. Connect the Data Pod to your Swarm in the Sources Menu of the data pod.
2. Create a Raw Table and subscribe to the given topic.

Then the Raw Table will accumulate all the published data from all devices in the swarm.
Note that the originating Device Serial and Device Name are always contained in the message.

# Privacy

The app runs on the edge close to the camera and only provides the detection information to subscribed clients.
The video footage itself is neither recorded nor sent to the cloud.

This ensures the conformity with privacy regulations like the GDPR.

# Production Use

For production use it is advised to create and maintain a new app for each model. 
So different apps for e.g. hard hat detection, people counting, plant detection and so on.

This would also allow you to run multiple models on the same device at the same time.

In production you might want to send the data to different platforms. 
For this you can add code in your custom app to send e.g. MQTT messages to Azure IoT.
# Requirements

This App was tested on

- NVIDIA Jetson Nano
- NVIDIA AGX Xavier

with
- USB Camera
- IP Camera