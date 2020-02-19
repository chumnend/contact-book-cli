MODULE_NAME = contacts

.PHONY: init
init:
	@pipenv install --three -r requirements.txt
	@pipenv shell
	
.PHONY: test
test:
	nosetests