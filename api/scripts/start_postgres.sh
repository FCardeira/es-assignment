#!/usr/bin/env bash

# Make sure to create volume first
# docker volume create postgres-volume

docker run --name my-postgres --env POSTGRES_PASSWORD=admin --volume postgres-volume:/var/lib/postgresql/data --publish 5432:5432 --detach postgres
