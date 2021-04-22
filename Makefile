install:
	rm -rf Pipfile.lock
	pipenv install -d

test:
	pipenv run python -m unittest src -v

run:
	pipenv run python -m src.main