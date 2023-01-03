# Star Wars Explorer

Web application allowing to collect, resolve and inspect information about characters
in the Star Wars universe from the [SWAPI](https://pipedream.com/apps/swapi).   

**Tech Stack:** Django, Django Rest Framework, Vue.js, Docker

<br>

# Installation

Application can be installed and run using Docker or virtual environment.

## 1. Docker

### Prerequisites:
- Docker (docker-compose)


Start the database and application:
```shell
docker-compose up
```

Containers can be afterwards removed with:
```shell
docker-compose down
```

## 2. Virtual environment (such as [venv](https://docs.python.org/3/library/venv.html))
 
<br>

This way will require creating [PostgreSQL](https://www.postgresql.org) and providing its credentials in `DATABASES` section of `sw_backend/settings/base.py`

<br>

> python3 -m venv \<environment-name\>

Environment activation on Linux/Mac:
> source \<environment-name\>/bin/activate

Environment activation on Windows:
> \<environment-name\>\Scripts\activate.bat

Required libraries are listed in the **requirements.txt** file included in this repository.  
**After activating** the environment run: 

> pip install -r requirements.txt

> python sw_backend/manage.py migrate

The app is running on a local server (by default http://127.0.0.1:8000/) that can be started by running:
> python sw_backend/manage.py runserver

<br>

# Usage
 
Having server running please visit http://127.0.0.1:8000/.<br>
You will be taken to the main page of the application, where you can see and download previously collected csv, or fetch and save fresh data.<br>
From there you can display details of given collection, by entering one of listed links.<br>
In the detail view you have 2 options - display all available data (loaded from the file by 10) or display aggregated data, according to selected columns.

<br>

Frontend application is comunicating with backend by REST API calls.<br>
To display list of available endpoints please visit [docs](http://127.0.0.1:8000/docs/).
