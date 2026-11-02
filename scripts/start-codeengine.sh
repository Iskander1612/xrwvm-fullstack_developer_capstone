#!/bin/bash
set -euo pipefail
mkdir -p /data/db
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-$(python -c 'import secrets; print(secrets.token_urlsafe(48))')}"
export MONGODB_URI=mongodb://127.0.0.1:27017/dealershipsDB
export BACKEND_URL=http://127.0.0.1:3030
export SENTIMENT_URL=http://127.0.0.1:5050
mongod --dbpath /data/db --bind_ip 127.0.0.1 --logpath /data/db/mongod.log --fork
node database/app.js &
(cd djangoapp/microservices && gunicorn --bind 127.0.0.1:5050 app:app) &
python manage.py migrate --noinput
python manage.py seed_cars
python - <<'PY'
import time, requests
for attempt in range(60):
    try:
        if requests.get('http://127.0.0.1:3030/fetchDealers',timeout=2).ok:
            break
    except requests.RequestException:
        pass
    time.sleep(1)
else:
    raise SystemExit('Dealership API did not become ready')
PY
exec gunicorn djangoproj.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --access-logfile -
