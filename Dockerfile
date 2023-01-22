FROM python:3.9
COPY requirements.txt requirements.txt
COPY token.json token.json
COPY gfpgan gfpgan
COPY realesrgan realesrgan
COPY src src

RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "telegram-api.py"]