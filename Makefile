.PHONY: test

test:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals .
