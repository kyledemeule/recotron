SHELL = /bin/bash

server:
	FLASK_APP=app.py FLASK_ENV=development flask run --port 5000

deploy:
	git push heroku master

env:
	source venv/bin/activate

