# News Application

This project is a minimal Django news application with:

- custom users and roles
- publishers, articles, and newsletters
- approval flow for articles
- REST API endpoints for articles and newsletters

## Run locally

1. Activate the virtual environment.
2. Run `python manage.py migrate`.
3. Run `python manage.py runserver 127.0.0.1:8001`.
4. Open http://127.0.0.1:8001/.

## Test

Run:

```bash
python manage.py test news_app
```
