.PHONY: test-openshift-4

test-openshift-4:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals .
