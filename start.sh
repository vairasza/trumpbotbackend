docker build -t trumpbot_backend .
docker run -p 5037:5037 -d trumpbot_backend