#!/usr/bin/env bash

echo "Apply database migrations"
./bin/wait-for-it.sh -t 5 db:5432 -- echo "✅ DB is up"

COUNTER=0

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

python manage.py checkadmin

if [ $? -eq 0 ]; then
  echo "✅ Admin already present"
else
  echo "🧑‍💻 Creating superuser"
  python manage.py createsuperuser --noinput
fi

python manage.py runserver 0.0.0.0:8000 --settings=pose.settings.dev

exec "$@"