# Roboflow Model Tester

This App allows you to use models from the Roboflow Vision AI platform on your camera Swarm. The Roboflow platform has a library with a lot of readily trained models provided by the community.

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

# Data Collection

The models provide the detection results as a json file that can be sent to a Data Pod within the platform.

To publish data this app uses the integrated WAMP message broker and uses the Topic given by you in the paramters of the App.

Parameter | Description
--- | ---
Publish Topic | The topic under which subscribers in a Data Pod can receive the data.

To receive the json data in a Data Pod you need to 

1. Connect the Data Pod to your Swarm in the Sources Menu of the data pod.
2. Create a Raw Table and subscribe to the given topic.

Then the Raw Table will accumulate all the published data from all devices in the swarm.
Note that the originating Device Serial and Device Name are always contained in the message.

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