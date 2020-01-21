FROM python:3.7.4

WORKDIR /DVBGServer

COPY requirements.txt /DVBGServer
RUN pip install -r requirements.txt

COPY . /DVBGServer

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]