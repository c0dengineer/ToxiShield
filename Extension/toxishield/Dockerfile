FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask flask-cors torch transformers sentencepiece

CMD ["python", "app.py"]
