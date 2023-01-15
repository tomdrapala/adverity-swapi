# Star Wars Explorer

Web application allowing to collect, resolve and inspect information about characters
in the Star Wars universe from the [SWAPI](https://pipedream.com/apps/swapi).   

**Tech Stack:** Django, Django Rest Framework, Vue.js, Docker

<br>

# Installation

### Prerequisites:
- Docker (docker-compose)

Start the database and application:
```shell
docker-compose up
```

The application can be stopped with the removal of the containers by the command:
```shell
docker-compose down
```

# Usage
 
Having server running please visit http://127.0.0.1:8000/.<br>
You will be taken to the main page of the application, where you can see and download previously collected csv, or fetch and save fresh data.<br>
From there you can display details of given collection, by entering one of listed links.<br>
The application will start with examplary object in the database and CSV file available.<br>
In the detail view you have 2 options - display all available data (loaded from the file by 10) or display aggregated data, according to selected columns.

<br>

Frontend application is comunicating with backend by REST API calls.<br>
To display list of available endpoints please visit [docs](http://127.0.0.1:8000/docs/).
