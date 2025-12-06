#!/usr/bin/env bash

# where the project resides inside docker
DOCKER_ROOT="/jetson-voice"	

PWD="/home/jetson/rover/jetson-voice"

# generate mount commands
DATA_VOLUME="--volume $PWD/data:$DOCKER_ROOT/data"
DEV_VOLUME=""

# parse user arguments
USER_VOLUME="-v $PWD/VoiceNav:$DOCKER_ROOT/VoiceNav"
USER_COMMAND="python3 VoiceNav/voic.py"

TAG="r32.7.1"
CONTAINER_NAME="dustynv/jetson-voice"
CONTAINER_IMAGE="$CONTAINER_NAME:$TAG"



MOUNTS="\
--device /dev/snd \
--device /dev/bus/usb \
--volume /etc/timezone:/etc/timezone:ro \
--volume /etc/localtime:/etc/localtime:ro \
$DEV_VOLUME \
$DATA_VOLUME \
$USER_VOLUME"

docker run --name voice-nav --runtime nvidia   --network host \
	$MOUNTS $CONTAINER_IMAGE $USER_COMMAND
