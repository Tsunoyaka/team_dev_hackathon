run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

restartdb:
	dropdb spotify_db
	createdb spotify_db
	python3 manage.py makemigrations account
	python3 manage.py makemigrations music
	python3 manage.py makemigrations album
	python3 manage.py migrate
	python3 manage.py createsuperuser

