SRC_DIR ?= ./src
BIN_DIR ?= ./bin

$(BIN_DIR)/zhunt: $(SRC_DIR)/zhunt3.c
	gcc -o $@ $<

all: $(BIN_DIR)/zhunt

clean:
	rm $(BIN_DIR)/zhunt
