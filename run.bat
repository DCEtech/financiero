START /B docker-compose up > docker.output 2>&1

flet run app/main.py

docker-compose down
exit
