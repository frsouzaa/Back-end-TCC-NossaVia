#!/bin/bash

echo "Iniciando container do PostgreSQL para realização dos testes"

container_id=$(docker run -d -p 12345:5432 \
-e POSTGRES_DB="test_db" \
-e POSTGRES_USER="test_user" \
-e POSTGRES_PASSWORD="test_pass" \
postgres:16)

docker_ready=$(docker exec $container_id pg_isready);

while [ $? != "0" ]
do
    docker_ready=$(docker exec $container_id pg_isready);
    sleep 0.1;
done

echo "Container $container_id iniciado com sucesso"

coverage run -m pytest -sx

echo "Finalizando container de testes do PostgreSQL"

container_id=$(docker rm $container_id -f)

echo "Container $container_id finalizado com sucesso"

coverage html
