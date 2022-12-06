FROM osgeo/gdal

ENV DEBIAN_FRONTEND noninteractive

USER root

RUN mkdir -p /usr/src/backend

COPY requirements.txt /usr/src/requirements.txt

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install python3.9 -y
RUN apt install python3-pip -y

#install python packages
RUN pip3 install --no-cache-dir -r /usr/src/requirements.txt

#add backend
COPY ./backend /usr/src/backend

CMD [ "python3", "usr/src/backend/app.py"]

EXPOSE 5050/udp
EXPOSE 5050/tcp