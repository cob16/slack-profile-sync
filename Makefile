test:
	poetry run pytest --block-network

test-and-record:
	 poetry run pytest --record-mode=once #rewrite is also a valid arg