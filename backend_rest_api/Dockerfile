FROM python:3.9-slim

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "./run.sh"]
