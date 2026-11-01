# Back-End-Development-Pictures

Flask REST API completed from the IBM Skills Network course template.

## Environment setup

The course Cloud IDE can initialize Python 3.9 with `bash bin/setup.sh` and
its `backend-pics-venv` environment. This implementation
was also verified locally with Python 3.12 and the pinned requirements.

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -v
gunicorn --bind 127.0.0.1:3000 app:app
```

## API

`GET /health`, `GET /count`, `GET /picture`,
`GET /picture/<id>`, `POST /picture`,
`PUT /picture/<id>`, and `DELETE /picture/<id>`.

Picture data is held in memory and resets when the process restarts.
