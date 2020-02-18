MODULE_NAME = template

.PHONY: init
init:
	@pipenv install --three -r requirements.txt
	@pipenv shell
	
.PHONY: start
start:
	@python -m $(MODULE_NAME)

.PHONY: test
test:
	nosetests