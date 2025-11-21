# website

Personal site + ML playground powered by a Vue 3 frontend and a small Flask
server. The Flask app serves the compiled Vue bundle and exposes links to an
external Model Zoo demo (`https://modelzoo.app`). A Heroku-friendly setup
(`Procfile`, `runtime.txt`, `requirements.txt`) is included so everything can
be deployed as-is.

## Local development

### Frontend

```bash
cd frontend
npm install        # first run only
npm run serve      # starts Vite dev server with hot reload
```

### Backend

The backend assumes the Vue app has been built to `frontend/dist`.

```bash
cd frontend
npm run build      # outputs production bundle into frontend/dist
cd ..
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py      # serves the built bundle at http://localhost:5000
```

## Deploying to Heroku

1. Ensure `frontend/dist` contains the latest production build (`npm run build`).
2. Commit the generated assets along with the Python sources.
3. Create the Heroku app with the Python buildpack (gunicorn is configured in
   `Procfile`).
4. Push the repository to Heroku: `git push heroku main`.

Heroku will install the dependencies from `requirements.txt` and launch the app
with `gunicorn app:app`, which serves the static Vue files directly.
