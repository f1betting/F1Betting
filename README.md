# F1Betting

An API to do bets with your friends about F1 race results!

## Docker
Build image using
````shell
$ docker build -t f1betting .
````


Run container using:
````shell
$ docker run --env-file ./.env -d --name f1betting -p 8001:80 f1betting
````