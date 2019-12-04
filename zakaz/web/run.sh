#!/usr/bin/env bash
docker run --rm --name taos_postgres -e POSTGRES_USER=order -e POSTGRES_DB=order -e POSTGRES_PASSWORD=order -p 6556:5432 postgres
#docker run --rm --name taos_postgres -e POSTGRES_DB=order -p 6556:5
# 432 postgres
