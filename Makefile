install:
	python -m pip install -r requirements.txt

lint:
	pylint --disable=R,C  app.py

test:
	pytest -vv