.PHONY: test test-httpd test-php test-perl test-mariadb test-mysql test-nginx test-postgresql test-redis test-all test-nodejs test-ruby test-python

test:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_varnish_*.py

test-httpd:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_httpd_*.py

test-mariadb:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_mariadb_*.py

test-mysql:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_mysql_*.py

test-nginx:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_nginx_*.py

test-postgresql:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_postgresql_*.py

test-redis:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_redis_*.py

test-php:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_php_*.py

test-perl:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_perl_*.py

test-nodejs:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_nodejs_*.py

test-python:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_python_*.py

test-ruby:
	cd tests && PYTHONPATH=$(CURDIR) python3.12 -m pytest --color=yes -s -rA --verbose -vv --showlocals test_ruby_*.py

test-all: test test-php test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis test-perl test-python test-ruby test-nodejs

test-nons2i: test test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis

test-s2i: test-php test-perl test-nodejs test-python test-ruby
