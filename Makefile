SRC_DIR ?= ./src
BIN_DIR ?= ./bin
SHELL ?= bash
GCC ?= gcc
SCRIPTS ?= ./scripts

$(BIN_DIR)/zhunt: $(SRC_DIR)/zhunt3.c
	$(GCC) -o $@ $<

all: $(BIN_DIR)/zhunt

clean:
	rm $(BIN_DIR)/zhunt

tests: $(BIN_DIR)/zhunt
	$(SHELL) $(SCRIPTS)/example_run.sh
