# Base image
FROM donaurelio/datacube-bac:1.8.2

# Image propietary
LABEL maintainer="Aurelio Vivas aa.vivas@uniandes.edu.co"

# Disable interctaive installs
ENV DEBIAN_FRONTEND=noninteractive

# postgresql
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

USER datacube

RUN git clone https://github.com/opendatacube/datacube-explorer.git \
    && cd datacube-explorer \
    && pip install -e . \
    && pip install gunicorn

COPY docker-entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
