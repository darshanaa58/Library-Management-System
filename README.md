# Library Management System

This is the repository for Library Management System 

### Requirements
--------------------------

* Python > 3


### How to run backend using make
--------------------------


```bash
python3 -m venv venv
source venv/bin/activate
make build
make makemigrations [only if there are database changes]
make migrate
make run
```

You can go to `localhost:9000` to access the backend application.
### How to run backend normally without make
--------------------------

```bash
python3 -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrate
python manage.py runserver 9000
```



### How to run tests
--------------------------

```bash
make test or python manage.py test management_system.tests
```


### API endpoint documentation
--------------------------

You can access the swagger documentation for api endpoints by going to ```localhost:9000/api/docs```
