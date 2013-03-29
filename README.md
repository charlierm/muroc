muroc
=====

Moruc V2

Proof of concept django site for corum

##Requirements:
* Celery (http://www.celeryproject.org)
* Django-Celery (https://pypi.python.org/pypi/django-celery)
* BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)

###Running:
The celery worker needs to be started before using the site, to start it run:
```
python manage.py celery worker --loglevel=info
```
Then start the server normally with
```
python manage.py runserver
```
