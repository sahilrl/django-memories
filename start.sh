#!/bin/bash
cd ..
if [ ! -d "env" ]
then
	virtualenv env
fi
#> .env
#echo "SECRET_KEY=owd(d$r!@bu93===j41@ws*0(p+qbaw0fq+r7)(#gwiwrut629" >> .env
#echo "EMAIL_HOST_USER='xyz@gmail.com'" >> .env
#echo "EMAIL_HOST_PASSWORD='xyz'" >> .env
#echo "DEBUG=True" >> .env
#echo "ALLOWED_HOSTS='localhost'" >> .env
#echo "SECURE_SSL_REDIRECT=False" >> .env
source env/bin/activate
cd django-memories
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

