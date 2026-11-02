# fullstack_developer_capstone

## Best Cars — Cars Dealership Portal

Full-stack capstone application by Iskander Akipov, based on the IBM Skills Network starter.

### Architecture

- React: responsive dealer catalog, state filtering, authentication, dealer reviews, and review submission.
- Django / SQLite: users, sessions, admin, and car makes/models.
- Node.js / Express / MongoDB: dealership and review persistence. Initial data loads idempotently.
- Flask / NLTK VADER: sentiment analysis using the bundled lexicon.
- GitHub Actions: build, Django checks/tests, Node syntax, sentiment check.
- Docker Compose and Kubernetes deployment template.

### Run with Docker

Set a random `DJANGO_SECRET_KEY` in an untracked `.env` file, then run `docker compose up --build`.
Open http://localhost:8000. Run `docker compose exec web python manage.py createsuperuser` to create an admin account.

### Run locally

1. Create a Python 3.13 virtual environment and install `server/requirements.txt` and `server/djangoapp/microservices/requirements.txt`.
2. Start MongoDB. Set `MONGODB_URI` for the Node service if it differs from `mongodb://127.0.0.1:27017/dealershipsDB`.
3. In `server/database`, run `npm ci && node app.js` (port 3030).
4. In `server/djangoapp/microservices`, run `python app.py` (port 5050).
5. In `server/frontend`, run `npm ci && npm run build`.
6. In `server`, run `python manage.py migrate && python manage.py seed_cars && python manage.py runserver 8000`.

Set `BACKEND_URL`, `SENTIMENT_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `DJANGO_SECRET_KEY` for a deployed environment. Turn off debug with `DJANGO_DEBUG=0`. Set `DATABASE_PATH` to a persistent SQLite path.

### Validation

`cd server && python manage.py test djangoapp -v 2`

The workflow `.github/workflows/ci.yml` runs validation on pushes and pull requests.

### Image credits

Photography served from Unsplash: car photo by [Campbell](https://unsplash.com/photos/3ZUsNJhi_Ik); additional portrait/team photography from Unsplash. Team names and contact details on the demo About/Contact pages are illustrative.

### Submission evidence

Evidence is generated from real executions and browser interactions and stored locally under `submission/` (ignored by Git). Deployment URLs and CI results are recorded only after successful execution.
