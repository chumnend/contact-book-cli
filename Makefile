MODULE_NAME = contacts

.PHONY: init
init:
	@pipenv install --three -r requirements.txt
	@pipenv shell
	
.PHONY: build 
build:
	@python setup.py build

.PHONY: install
install: 
	@python setup.py install

.PHONY: test
test:
	nosetests
	
.PHONY: clean
clean:
	rm -rf build dist *.egg *.egg-info