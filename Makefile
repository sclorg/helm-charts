.PHONY: test_varnish test-httpd test-php test-perl test-mariadb test-mysql test-nginx test-postgresql test-redis test-all test-nodejs test-ruby test-python test-valkey test-all-imagestreams

test_varnish:
	tests/run-pytest varnish

test-httpd:
	tests/run-pytest httpd

test-mariadb:
	tests/run-pytest mariadb

test-mysql:
	tests/run-pytest mysql

test-nginx:
	tests/run-pytest nginx

test-postgresql:
	tests/run-pytest postgresql

test-redis:
	tests/run-pytest redis

test-php:
	tests/run-pytest php

test-perl:
	tests/run-pytest perl

test-nodejs:
	tests/run-pytest nodejs

test-python:
	tests/run-pytest python

test-ruby:
	tests/run-pytest ruby

test-valkey:
	tests/run-pytest valkey

test-all-imagestreams:
	tests/run-pytest imagestreams

test-all: test test-php test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis test-perl test-python test-ruby test-nodejs test-valkey

test-nons2i: test test-httpd test-mariadb test-mysql test-nginx test-postgresql test-redis

test-s2i: test-php test-perl test-nodejs test-python test-ruby
