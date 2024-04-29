install:
	python -m pip install -r requirements.txt

lint:
	pylint --disable=R,C  flask_app.py

test:
	pytest -vv