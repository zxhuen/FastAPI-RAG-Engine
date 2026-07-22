## docker compose up --build -d

## development

docker compose up -d redis
celery -A app.core.celeryapp worker --pool=solo --loglevel=info

## dockerized

docker compose up --build -d
