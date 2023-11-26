FROM rabbitmq

# Define environment variables.
COPY ./docker/local/rabbitmq/start.sh /start.sh
RUN sed -i 's/r$//g' /start.sh
RUN chmod +x /start.sh