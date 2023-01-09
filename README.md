# Roboflow Example App

This App uses a model developed on the Roboflow Vision AI platform.

When the App starts it downloads the model data from the roboflow platform and uses a local inference engine to execute the model based on the video data from the attached camera.

This App can take your roboflow API key and the model and version as input parameters so it can serve as a universal app to execute all your Roboflow models on your swarm of edge devices.

For production use it is advised to create and maintain a new app for each model. So e.g. different apps for hard hat detection, people counting, object classification and so on.

This would also allow you to run multiple models one one device at the same time.

# Requirements

This App was only tested on Nvidia Jetson AGX together with an IP-Camera.