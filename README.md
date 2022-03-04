## Django Starter Template ##

The project contains 3 apps:

- accounts (for user register, login, logout, forgot password) (Using Django REST and GraphQL)
- chat (one to one chat) (Using Django Channels)
- crud_operation (Basic CRUD operations performed on Task model using Django REST)

Steps to follow:

1 - create conda env with python version using:

conda create -n myenv python=X.Y  # Replace "X.Y" as appropriate

2 - activate env:

conda activate myenv

3 - Point your terminal path to project folder

4 - Install packages from requirements.txt using:

pip install -r requirements.txt
or
conda install --file requirements.txt

5 - To create a super-user:

python manage.py create superuser

6 - To make app specific migrations:

python manage.py makemigrations app_name

7 - After all app specific migrations are done:

python manage.py migrate

8 - Run server:

python manage.py runserver

9 - To deactivate env:

conda deactivate