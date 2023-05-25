docker build -t trumpbot_backend .
docker run -p 5037:5037 -d trumpbot_backend

#!/bin/bash
APP_NAME="trumpbot_backend"

OLD_ID=$(docker ps -qaf "name=$APP_NAME")
if [ ! -z $OLD_ID ];
then docker stop $OLD_ID;
fi

REMOVEABLE_IMAGES=$(docker images --filter dangling=true -q)
if [ ! -z $REMOVEABLE_IMAGES ];
then docker rmi $REMOVEABLE_IMAGES -f;
fi

docker build --rm -t $APP_NAME .
IMAGE_ID=$(docker images -q $APP_NAME)
docker run --rm -d -p $TRUMPBOT_BACKEND_PORT:$TRUMPBOT_BACKEND_PORT --name $APP_NAME $IMAGE_ID