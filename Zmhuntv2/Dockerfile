FROM ubuntu:latest

ENV ZHUNT_HOME=/zhunt
ARG GCC_OPTS="-lm"
ARG REQUIREMENTS=requirements.txt
ARG RREQUIREMENTS=install_packages.R

# Credit to
# https://stackoverflow.com/questions/54437030/how-can-i-create-a-docker-image-to-run-both-python-and-r
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
                                               r-base \
                                               r-cran-randomforest \
                                               python3.6 \
                                               python3-pip \
                                               python3-setuptools \
                                               python3-dev \
                                               gcc
# -----------------------------------------------------------------------------

# Install all requirements.txt
# Copy zhunt source from build context
# Compile zhunt from source in this ubuntu environment

RUN mkdir -p $ZHUNT_HOME/bin\
    mkdir -p $ZHUNT_HOME/test\
    mkdir -p $ZHUNT_HOME/src

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers

# python dependency installs
COPY $REQUIREMENTS $ZHUNT_HOME/$REQUIREMENTS
RUN python3 -m pip install -r $ZHUNT_HOME/$REQUIREMENTS

# R dependency installs
COPY $RREQUIREMENTS $ZHUNT_HOME/$RREQUIREMENTS
RUN Rscript $ZHUNT_HOME/$RREQUIREMENTS

# path changes
ENV PYTHONPATH $PYTHONPATH:$ZHUNT_HOME
ENV PATH $PATH:$ZHUNT_HOME/bin

# add source code and tests
COPY test $ZHUNT_HOME/test
COPY src $ZHUNT_HOME/src

# compile zhunt with gcc
RUN gcc -o $ZHUNT_HOME/bin/zhunt $ZHUNT_HOME/src/zhunt3.c -lm
RUN gcc -o $ZHUNT_HOME/bin/mhunt $ZHUNT_HOME/src/mhunt.c -lm

WORKDIR $ZHUNT_HOME

COPY . .
CMD ["flask", "run"]
