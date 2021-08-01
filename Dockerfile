FROM postgres:alpine

RUN mkdir -p /app

WORKDIR /app

COPY ./tools/create_postgres_db.sql /app

RUN echo 'psql -a -f /app/create_postgres_db.sql' >> /docker-entrypoint-initdb.d/init-user-db.sh
