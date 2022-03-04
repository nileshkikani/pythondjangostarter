# Reference

1. https://simpleisbetterthancomplex.com/series/2017/09/04/a-complete-beginners-guide-to-django-part-1.html
2. https://www.javatpoint.com/django-tutorial
3. https://tutorial.djangogirls.org/en/
4. https://overiq.com/django-1-11/

==================================================================================================

# Installation

1. python -m pip install Django

2. check Django version
   django-admin --version

# Installing Virtualenv

- https://simpleisbetterthancomplex.com/series/2017/09/04/a-complete-beginners-guide-to-django-part-1.html#installing-virtualenv

- sudo pip3 install virtualenv
- cd project

- create vertualenv folder
    virtualenv --system-site-packages templatevenv   (Your System package install)
    OR
    virtualenv templatevenv -p python3 (Install manually)

- If error generate to run project for six
     pip install --ignore-installed six

- active virtualenv
    source templatevenv/bin/activate
    ./manage.py runserver
    
- deactive virtualenv    
    deactivate
    
# Create Project

1. django-admin startproject projectName

# Run Project

1. python manage.py runserver

# Create app

1. django-admin startapp blog

# MySqlClient Installation (DATABASE CONNECTIVITY)

- Install mysqlClient
  pip install mysqlclient

- If error in brew
  sudo chown -R "\$(whoami)":admin /usr/local/lib

- # mysqlclient Installation Error
  A. brew install mysql-client
  B. echo 'export PATH="/usr/local/opt/mysql-client/bin:\$PATH"' >> ~/.bash_profile
  C. source ~/.bash_profile
  D. pip install mysqlclient

# Create migration

1.  python manage.py makemigrations
    OR
    python3 manage.py makemigrations
    OR
    ./manage.py makemigrations


2.  python manage.py migrate

# SCSS INSTALLATION

- https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/

1. pip install django_compressor
2. pip install django-libsass
3. add bootstrap(scss) folder in static folder
4.  run command
    python manage.py compress

# requirements.txt (packages list)
- create this file at root level
- pip install -r requirements.txt
- pip freeze > requirements.txt

# .env file or more
- https://github.com/henriquebastos/python-decouple
- pip install python-decouple

# REST FRAMEWORK (API)
- https://www.django-rest-framework.org/

