SERID=$(shell id -u)
GROUPID=$(shell id -g)

help:
	@echo 'Available commands:'
	@echo ''
	@echo 'build ................................ Install required packages'
	@echo 'run .................................. Runs the webserver'
	@echo 'test ................................. Runs all tests except integration'
	@echo ''

build:
	pip install -r requirements.txt

test:
	python manage.py test management_system.tests

run:
	python manage.py runserver 9000

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

.PHONY: all build test run makemigrations migrate