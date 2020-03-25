# FROM python:3
# USER root
# WORKDIR /app
# ADD . /app
# RUN pip install  -r requirements.txt
# CMD [ "python", "./log_service.py" ]


FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app2
WORKDIR /app2
COPY requirements.txt /app2/
RUN pip install -r requirements.txt
COPY . /app2/