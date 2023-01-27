FROM python:3.9
COPY requirements.txt requirements.txt
COPY src src

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY inputs inputs
ENTRYPOINT ["python3", "src/telegram-api.py"]