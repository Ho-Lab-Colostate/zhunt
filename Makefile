#run with make -f Makefile
SRC_DIR ?= /Users/Team_HoLab/Desktop/RSC/Documents/Coding/Zhunt
BIN_DIR ?= /usr/local/bin
SHELL ?= bash
GCC ?= gcc
SCRIPTS ?= ./scripts
PYTEST_DIR ?= $(SRC_DIR)/tests
PREF_SHELL ?= bash
GITREF=$(shell git rev-parse --short HEAD)
GITREF_FULL=$(shell git rev-parse HEAD)

####################################
# Compile C
####################################
GCC_OPTS ?= -lm

$(BIN_DIR)/zhunt: $(SRC_DIR)/zhunt3.c
	$(GCC) $(GCC_OPTS) -o $@ $<

all: $(BIN_DIR)/zhunt

clean:
	rm $(BIN_DIR)/zhunt

tests: $(BIN_DIR)/zhunt
	$(SHELL) $(SCRIPTS)/example_run.sh

####################################
# Docker image
####################################

IMAGE_ORG ?= enho
IMAGE_NAME ?= zhunt
IMAGE_TAG ?= 0.0.1
IMAGE_DOCKER ?= $(IMAGE_ORG)/$(IMAGE_NAME):$(IMAGE_TAG)
IMAGE_DOCKER_DEV ?= $(IMAGE_ORG)/$(IMAGE_NAME):$(GITREF)
IMAGE_SIMG ?= $(IMAGE_ORG)-$(IMAGE_NAME)-$(IMAGE_TAG).simg
IMAGE_SIMG_DEV ?= $(IMAGE_ORG)-$(IMAGE_NAME)-$(GITREF).simg
IMAGE_SRC_DIR ?= /zhunt
IMAGE_PYTEST_DIR ?= $(IMAGE_SRC_DIR)/test

####################################
# Runtime arguments
####################################

DOCKER_OPTS ?= --rm -v ${PWD}/outputs:$(IMAGE_SRC_DIR)/outputs \
	-v ${PWD}/inputs:$(IMAGE_SRC_DIR)/inputs \
	-e GITREF=$(GITREF)

####################################
# Sanity checks
####################################

PROGRAMS := git docker python poetry singularity
.PHONY: $(PROGRAMS)
.SILENT: $(PROGRAMS)

docker:
	docker info 1> /dev/null 2> /dev/null && \
	if [ ! $$? -eq 0 ]; then \
		echo "\n[ERROR] Could not communicate with docker daemon. You may need to run with sudo.\n"; \
		exit 1; \
	fi
python poetry singularity:
	$@ -h &> /dev/null; \
	if [ ! $$? -eq 0 ]; then \
		echo "[ERROR] $@ does not seem to be on your path. Please install $@"; \
		exit 1; \
	fi
git:
	$@ -h &> /dev/null; \
	if [ ! $$? -eq 129 ]; then \
		echo "[ERROR] $@ does not seem to be on your path. Please install $@"; \
		exit 1; \
	fi

####################################
# Build Docker image
####################################
.PHONY: image image-dev shell tests pytest-docker clean clean-image clean-tests
# .SILENT: image

requirements.txt: | poetry
	poetry export --without-hashes -f requirements.txt -o $@

requirements-dev.txt: | poetry
	poetry export --dev --without-hashes -f requirements.txt -o $@

image: ./Dockerfile requirements.txt | docker
	docker build --build-arg REQUIREMENTS=$(word 2,$^) \
		-t $(IMAGE_DOCKER) -f $< .

image-dev: ./Dockerfile requirements-dev.txt | docker
	docker build --build-arg REQUIREMENTS=$(word 2,$^) \
		-t $(IMAGE_DOCKER_DEV) -f $< .

deploy: image | docker
	docker push $(IMAGE_DOCKER)

deploy-dev: image-dev | docker
	docker push $(IMAGE_DOCKER_DEV)

####################################
# Tests in Docker container
####################################

shell: image | docker
	docker run -it $(DOCKER_OPTS) $(IMAGE_DOCKER) bash

tests: tests-main

tests-main: image | docker
	docker run $(DOCKER_OPTS) $(IMAGE_DOCKER) \
		$(PYTHON) --version

tests-bin: image | docker
	docker run $(DOCKER_OPTS) $(IMAGE_DOCKER) \
		zhunt 12 6 12 $(IMAGE_PYTEST_DIR)/data/example_input0.fasta

pytest: pytest-docker

pytest-docker: image-dev | docker
	docker run $(DOCKER_OPTS) \
		$(IMAGE_DOCKER_DEV) \
		$(PYTHON) -m pytest $(IMAGE_PYTEST_DIR)

clean: clean-tests

clean-image:
	docker rmi -f $(IMAGE_DOCKER)

clean-tests:
	rm -rf .hypothesis .pytest_cache __pycache__ */__pycache__ \
		tmp.*
