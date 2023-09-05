# goit_python_web_hw_04

## RUN WEB SERVER

```
 python  webapp/app.py
```

## INDEX

![Index](doc/app-index.png)

## MESSAGE

### MESSAGE FORM

![Index](doc/app-message.png)

 
### MESSAGE POST

![Index](doc/app-message-post.png)




## DOCKER

## dockerfile

```
FROM python:3.11-slim

ENV APP_HOME /app 

WORKDIR $APP_HOME

COPY . .

EXPOSE 3000/tcp

VOLUME $APP_HOME/storage

ENTRYPOINT [ "python", "webapp/app.py" ]

```

### BUILD
docker build . -t lexxai/web_hw_04

### RUN
docker run -it -d --rm -p 3000:3000  -v demo-web_hw_04_volume:/app/storage  --name web_hw_04  lexxai/web_hw_04     


