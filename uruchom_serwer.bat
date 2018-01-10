@echo off
python manage.py makemigrations stronka
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
cmd /k
