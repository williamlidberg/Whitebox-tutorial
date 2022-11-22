FROM osgeo/gdal:latest
RUN apt-get update
RUN apt-get update && apt-get install -y python3-pip
RUN pip install whitebox==2.0.3