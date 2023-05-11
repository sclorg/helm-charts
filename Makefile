.PHONY: test test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis test-all

test:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_varnish_*
test-httpd:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_httpd_*
test-mariadb:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_mariadb_*
test-mysql:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_mysql_*
test-nginx:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_nginx_*
test-postgresql:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_postgresql_*
test-redis:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals test_redis_*
test-all: test test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis
