# FROM python:3
# USER root
# WORKDIR /app
# ADD . /app
# RUN pip install  -r requirements.txt
# CMD [ "python", "./notes_service.py" ]


FROM python:3
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
RUN mkdir /app3
WORKDIR /app3
COPY requirements.txt /app3/
RUN pip install -r requirements.txt
COPY . /app3/