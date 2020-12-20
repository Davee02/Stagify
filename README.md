# Stagify

## Development

We recommend using the code editor [Visual Studio Code](https://code.visualstudio.com/) for developing and debugging Stagify.
After you opened the root folder of the project in Visual Studio Code install all the recommended extensions. You don't need to tweak additional settings because we're using the defaults.

The following softwares are required to run Stagify locally:

- [Python 3](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

You can proceed by running the Postgres database with docker compose:

```shell
docker-compose up -d
```

Then you can install all python packages, run the migrations and start the dev server for the backend:

```shell
cd ./stagifyapi
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For running the frontend you have to restore all node packages and start the dev server:

```shell
cd ../stagifyfrontend
npm i
npm start
```

The frontend is now available on `http://localhost:4200/`, the backend on `http://localhost:8000/`
