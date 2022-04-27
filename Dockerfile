FROM python:3.10

WORKDIR /home/nsu_app

COPY app/ ./app
COPY .ssl/ ./.ssl
COPY *.py .env requirements.txt ./
RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver"]
