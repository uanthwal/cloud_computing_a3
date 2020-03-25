# FROM python:3
# USER root
# WORKDIR /app
# ADD . /app
# RUN pip install  -r requirements.txt
# CMD [ "python", "./user_service.py" ]


FROM python:3
EXPOSE 5000
ENV PYTHONUNBUFFERED 1
RUN mkdir /app4
WORKDIR /app4
COPY requirements.txt /app4/
RUN pip install -r requirements.txt
COPY . /app4/