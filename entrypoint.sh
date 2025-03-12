#!/usr/bin/env bash

echo "Apply database migrations"
./bin/wait-for-it.sh -t 5 db:5432 -- echo "✅ DB is up"

COUNTER=0

# wait for db container
while
  python manage.py migrate --noinput
  M=$?
  [[ $M -eq 1 ]] && [ $COUNTER -lt 10 ]
do
  ((COUNTER++))
  echo "⚠️ couldn't migrate, trying again shortly"
  echo "    (attempt $COUNTER of 10)"
  sleep 3
done


# create superuser if necessary
python manage.py createsuperuser --noinput


# use wsgi in production
if [ ${ENV} = "production" ]; then
  gunicorn pose.wsgi:application --bind 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000 --settings=pose.settings.dev
fi

exec "$@"