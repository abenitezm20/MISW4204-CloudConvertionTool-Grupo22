# MISW4204-CloudConvertionTool-Grupo22
Repositorio para App Cloud Convertion Tool - Grupo 22

# Observaciones para developers
> docker compose --env-file .env.prod up (para ser utilizado en el server)
>
> docker compose -f docker-compose-pruebas.yml up (para entornos locales)
>
> docker compose down: detiene el docker
>
> docker compose build: cada vez que exista un cambio en el código, se debe ejecutar este comando antes de lanzar docker compose up

# Url base
> http://127.0.0.1:1337

# Para levantar solo el servidor de aplicacion de forma local
> gunicorn app:app -w 1 -b 0.0.0.0:8080

# Para construir la imagen de docker worker

> docker-compose
> -f docker-compose-worker.yml
> -f docker-compose-worker-gcp.yml
> build

# Para construir la imagen de docker app

> docker-compose
> -f docker-compose-app.yml
> -f docker-compose-app-gcp.yml
> build

# Para subir la imagen de docker worker

> docker-compose
> -f docker-compose-worker.yml
> -f docker-compose-worker-gcp.yml
> push

# Para subir la imagen de docker app

> docker-compose
> -f docker-compose-app.yml
> -f docker-compose-app-gcp.yml
> push
