.PHONY: test test-httpd test-php test-perl test-mariadb test-mysql test-nginx test-postgresql test-redis test-all test-nodejs test-ruby test-python

test:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_varnish_*

test-httpd:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_httpd_*

test-mariadb:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_mariadb_*

test-mysql:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_mysql_*

test-nginx:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_nginx_*

test-postgresql:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_postgresql_*

test-redis:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_redis_*

test-php:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_php_*

test-perl:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_perl_*

test-nodejs:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_nodejs_*

test-python:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_python_*

test-ruby:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose -vv --showlocals test_ruby_*

test-all: test test-php test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis test-perl test-python test-ruby test-nodejs

test-nons2i: test test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis

test-s2i: test-php test-perl test-nodejs test-python test-ruby
