#
# youtube-dl Server Dockerfile
#
# https://github.com/manbearwiz/youtube-dl-server-dockerfile
#

FROM python:alpine

RUN apk add --no-cache \
  ffmpeg \
  tzdata

# ENV FLASK_RUN_PORT=3001

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 3001

VOLUME ["/youtube-dl"]

# CMD [ "python", "-u", "./youtube-dl-server.py" ]
CMD [ "python", "-u", "./app.py" ]
# CMD [ "python", "app.py", "bdist_wheel" ]
# CMD [ "flask", "run" ]