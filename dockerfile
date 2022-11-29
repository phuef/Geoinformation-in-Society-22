FROM ubuntu

USER root

RUN mkdir -p /usr/src/backend
RUN mkdir -p /usr/src/data

COPY requirements.txt /usr/src/requirements.txt

#install gdal
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install python3.9 -y
#RUN add-apt-repository ppa:ubuntugis/ppa && add-apt-repository --remove ppa:ubuntugis/ppa && apt-get update
#RUN apt-get install -y python-numpy gdal-bin libgdal-dev python-gdal python3-gdal

#install python packages
#RUN pip3 install --no-cache-dir -r /usr/src/requirements.txt

#Add RDI
COPY ./backend/ /usr/src/backend
COPY ./data/ /usr/src/data
