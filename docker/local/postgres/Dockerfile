FROM postgres:15-bullseye

COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance

RUN chmod +x /usr/local/bin/maintenance/*

# Make scripts file available in $path
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
   && rmdir /usr/local/bin/maintenance