# It's necessary to set this because some environments don't link sh -> bash.
SHELL := /bin/bash

export PYTHONPATH=./

# We don't need make's built-in rules.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

clean:
	@rm -rf ./.cache \
			./src/__pycache__/ \
			./src/validators/__pycache__/ \
			./tests/__pycache__ \
			./tests/.cache \
			**/*.pyc

test: clean
	@pushd tests && python3.6 -m unittest discover -vvv

run:
	@python3.6 src/main.py

docker:
	@docker build . -t boranx/index-checker:1.0.0 -t boranx/index-checker:latest
	@docker push boranx/index-checker:1.0.0
	@docker push boranx/index-checker:latest

.DEFAULT_GOAL := run
.PHONY: clean, run, docker, test