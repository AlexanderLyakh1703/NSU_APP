FROM python:3.10

WORKDIR /home/app

COPY app *.py requirements.txt ./
RUN apt-get update
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver"]
