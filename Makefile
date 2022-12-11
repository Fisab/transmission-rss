

SHELL = /bin/bash

help:
	@echo "Targets:"
	@echo " "
	@echo "- make black"
	@echo "- make reqs"
	@echo " "

black:
	python3 -m black --skip-string-normalization .

reqs:
	poetry export -f requirements.txt --output requirements.txt
