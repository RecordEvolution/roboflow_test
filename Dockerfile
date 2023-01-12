FROM roboflow/inference-server:jetson

RUN apt-get --fix-broken install -y && apt-get update && apt-get install -y \
    software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.11 \
    libgl1
    
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

COPY requirements.txt ./

RUN python3.11 -m pip install -r requirements.txt

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]