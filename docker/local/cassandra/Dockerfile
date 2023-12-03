FROM cassandra:latest

COPY ./docker/scripts/wait-for-it.sh /wait-for-it.sh
RUN sed -i 's/\r$//g' /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./docker/local/cassandra/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/local/cassandra/schema.cql /schema.cql
RUN sed -i 's/\r$//g' /schema.cql

ENTRYPOINT [ "/entrypoint.sh" ]