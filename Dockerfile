FROM python:3.6
ENV ZHUNT_HOME=/zhunt
ARG GCC_OPTS="-lm"
ARG REQUIREMENTS=requirements.txt

RUN apt-get update && \
    apt-get -y upgrade && \
    mkdir -p $ZHUNT_HOME/bin

# python dependency installs
COPY $REQUIREMENTS $ZHUNT_HOME/$REQUIREMENTS
RUN pip install -r $ZHUNT_HOME/$REQUIREMENTS

# path changes
ENV PYTHONPATH $PYTHONPATH:$ZHUNT_HOME
ENV PATH $PATH:$ZHUNT_HOME/bin

# add source code and tests
COPY test $ZHUNT_HOME/test
COPY src $ZHUNT_HOME/src

# compile zhunt with gcc
RUN gcc $GCC_OPTS -o $ZHUNT_HOME/bin/zhunt $ZHUNT_HOME/src/zhunt3.c

WORKDIR $ZHUNT_HOME
