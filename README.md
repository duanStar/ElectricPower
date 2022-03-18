# ElectricPower

## Install
```shell
pip install django
pip install mysqlclient
pip install django-simpleui
# Above all are mainly for the env and components here.
```

> Note: The edition of Django is better to use >4.0 because of the admin-sys has some bugs before 4.0

## Step

* install the envs.
* setup and launch mysql8.
* check the settings.py for databases config.
* then, run：
```shell
python manage.py makemigrations
python migrate
```
* Thus, you can connect the database here.
* new terminal and run:
```shell
python manage.py runserver <127.0.0.1>:<PORT>
```
* click the address.