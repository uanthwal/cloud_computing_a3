# FROM python:3
# USER root
# WORKDIR /app
# ADD . /app
# RUN pip install  -r requirements.txt
# CMD [ "python", "./catalogue_service.py" ]

FROM python:3
EXPOSE 7000
ENV PYTHONUNBUFFERED 1
RUN mkdir /app1
WORKDIR /app1
COPY requirements.txt /app1/
RUN pip install -r requirements.txt
COPY . /app1/