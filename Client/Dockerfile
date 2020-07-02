FROM balenalib/rpi-python:3.7.2-stretch-build
# copy files
COPY . /home/Desktop/Client

# setup env
RUN usermod -a -G video root
RUN apt-get update && apt-get install -y \
    libraspberrypi-bin

# install python env
RUN /bin/bash -c 'source $HOME/.bashrc; bash /home/Desktop/Client/setup-client.bat'

# entry point
ENTRYPOINT ["python /home/Desktop/Client/socket_client_rpi.py"]
CMD ["--help"]