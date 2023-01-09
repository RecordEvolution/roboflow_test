FROM roboflow/inference-server:jetson

RUN apt-get --fix-broken install -y && apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt ./
RUN python3 -v
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY engine.py /app/engine.py
COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]