FROM alpine:latest
LABEL maintainer="Jimmi Kristensen <picbot@gmail.com>"

# Set language to avoid bugs that sometimes appear
ENV LANG en_US.UTF-8

# Set up requirements
RUN apk upgrade --update \
    && apk --no-cache add \
          python \
          py-pip \
          make \
          openjdk8-jre \
          ttf-dejavu \
          graphviz
	  
# Install PlantUML
RUN apk add --no-cache --virtual .ssl-deps \
      openssl \
      ca-certificates \
    && mkdir /opt \
    && wget -O "/opt/plantuml.jar" "https://sourceforge.net/projects/plantuml/files/plantuml.jar" \
    && printf '#!/bin/sh -e\njava -jar /opt/plantuml.jar "$@"' > /usr/local/bin/plantuml \
    && chmod 755 /usr/local/bin/plantuml \
    && apk del .ssl-deps \
    && mkdir /scripts

# Install Sphinx and extras
RUN pip install --no-cache-dir \
#      Sphinx \
      sphinx-confluence \
      sphinx_rtd_theme \
      sphinxcontrib-plantuml \
      sphinxcontrib-httpdomain \
      confluence-publisher

ADD sphinx_quickstart.sh /scripts
ADD confluence_publisher.sh /scripts
ADD confluencify_images.py /scripts
ADD confluence_config_creator.py /scripts

# Stop Java from writing files in documentation source
ENV _JAVA_OPTIONS -Duser.home=/tmp

# Set working directory to documentation root
WORKDIR /doc
