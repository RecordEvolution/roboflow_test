FROM roboflow/inference-server:jetson

RUN apt-get --fix-broken install -y && apt-get update && apt-get install -y \
    python3  \
    python3-pip  \
    python3-matplotlib

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip &&\
    python3 -m pip install -U setuptools &&\
    python3 -m pip install -r requirements.txt

COPY engine.py /app/engine.py
COPY wtf.py /app/wtf.py
COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]