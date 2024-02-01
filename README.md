# Library Management System

This is the repository for Library Management System 

### Requirements
--------------------------

* Python > 3


### How to run backend
--------------------------


```bash
python3 -m venv venv
source venv/bin/activate
make build
make makemigrations [only if there are database changes]
make migrate
make run
```

You can go to `localhost:{PORT_NUMBER}` to access the backend application.


### How to run tests
--------------------------

```bash
make test
```


### API endpoint documentation
--------------------------

You can access the swagger documentation for api endpoints by going to ```localhost:9000/api/docs```