FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /social_network
WORKDIR /social_network
ADD . /social_network/
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
