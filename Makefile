install: run-db
	poetry install

test:
	poetry run pytest

test-and-record:
	 poetry run pytest --record-mode=once #rewrite is also a valid arg

run-db:
	docker build -t posttest:local  .
	docker run --name posttest -d -p 5432:5432 -e POSTGRES_PASSWORD=pytestPassword posttest:local

stop-db:
	docker rm -f posttest

package:
	poetry run lambda-packager