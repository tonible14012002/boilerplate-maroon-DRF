FROM mcr.microsoft.com/mssql/server:latest

# add wait-for-it.sh script
# COPY ./docker/scripts/wait-for-it.sh /wait-for-it.sh
# RUN sed -i 's/\r$//g' /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh

COPY ./docker/local/mssql/run-initialization.sh /run-initialization.sh
RUN sed -i 's/\r$//g' /run-initialization.sh
RUN chmod +x /run-initialization.sh

COPY ./docker/local/mssql/create-database.sql /create-database.sql
RUN sed -i 's/\r$//g' /create-database.sql
RUN chmod +x /create-database.sql

COPY ./docker/local/mssql/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh