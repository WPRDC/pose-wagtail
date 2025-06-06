# CKAN Ecosystem Development Landing Page and Blog

https://civicdataecosystem.org

This site is built with [Wagtail](https://wagtail.org/) which is built on [Django](https://www.djangoproject.com/).

## Installation and Deployment

Deployment for this site is handled by [Docker Compose](https://docs.docker.com/compose/) so you'll need
to [install Docker ](https://docs.docker.com/get-started/get-docker/) as a prequisite.

1. Clone the repo
```shell
git clone git@github.com:WPRDC/pose-wagtail.git

# change directory to the repo
cd pose-wagtail
```

2. Create a `.env` file and edit it as needed. You can use our `.env.example` file to get started.

All configuration is done through environment variables. 

If you're deploying the site in production, make sure to set teh `ENVIROMENT` envar to "production"

See [Environment Variables section](#environment-variables) for details about each variable.

```shell
cp .env.example .env
vim .env  # or use your editor of choice
```

3. Build and deploy using Docker Compose
```shell
# in .../pose-wagtail/
docker compose up -d
```


## Environment Variables

```dotenv
# django secret key - make sure to replace with something secure in production
SECRET_KEY=django-insecure-al0ng@nd53cRe+K3y

# define how to to connect to the database
# if you're using the provided compose.yaml, you won't need to change the host or port.
DB_HOST=db
DB_PORT=5432

# you can values these names if necessary
DB_NAME=wagtail
DB_USER=wagtail

# while you won't expose the db to the public, you'll want to use something secure for a password
DB_PASSWORD=passw0rd

# catalog settings used to read data from the associated CKAN instance
CATALOG_HOST=https://catalog.civicdataecosystem.org
CATALOG_API_KEY='api-key-for-catalog'

# set to 'production' when running in production
# in production docker will use wsgi to serve the site and use production settings
ENVIRONMENT='development'

# used to create a superuser login on build
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=email@example.com
DJANGO_SUPERUSER_PASSWORD=password-for-admin

# set exposed ports - useful if the machine you're running on is already using the standard ports for something else
HOST_DJANGO_PORT=8000
HOST_DB_PORT=5432

# where static files will be stored on the host machine
STATIC_DIR=/var/www/html/static/
MEDIA_DIR=/var/www/html/media/

# API key to use MapTiler base maps (https://www.maptiler.com/)
MAPTILER_API_KEY=a_secret_key
```