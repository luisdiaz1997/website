# Luis F. Chumpitaz Diaz — Personal Site + Model Zoo

Live site: https://www.chumpitaz.com

Personal playground built with a Vue 3 SPA (Vue CLI) front-end and a small
Flask + PyTorch API that powers the digit-recognition demo. Production is served
with Gunicorn behind Nginx; Heroku support is included via `Procfile` and
`runtime.txt`.

## Stack
- Vue 3 + Vue Router + Vuex (`frontend/`)
- Flask API that loads a ResNet-34 classifier via PyTorch (`backend/`)
- Gunicorn for WSGI, optional Nginx reverse proxy
- Python 3.11 (`runtime.txt`), Node 16+ for the build tooling

## Install
```bash
# Frontend
cd frontend
npm install

# Backend
cd ..
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Local development
- Frontend dev server with hot reload:
  ```bash
  cd frontend
  npm run serve
  ```
- Backend (expects a built `frontend/dist`):
  ```bash
  cd frontend && npm run build
  cd ..
  source .venv/bin/activate
  python app.py  # http://localhost:5000
  ```

## Build the production bundle
```bash
cd frontend
npm run build      # outputs to frontend/dist
```

## Run the production server locally
```bash
source .venv/bin/activate
gunicorn app:app --bind 0.0.0.0:8000 --workers 2
# or python app.py for a single-process debug server
```

## Deploying

### Heroku
1. Build the Vue app: `cd frontend && npm run build`.
2. Commit `frontend/dist` and the backend files.
3. Push to Heroku (Python buildpack is picked up automatically): `git push heroku main`.
4. Heroku runs `gunicorn app:app` via `Procfile`.

### Linux + systemd + Nginx
1. Build the frontend (`npm run build`) and sync the repo to the server (keep `frontend/dist`).
2. Create the virtualenv and install deps:
   ```bash
   cd /opt/chumpitaz   # example path
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run Gunicorn (wrap it in systemd for persistence):
   ```bash
   /opt/chumpitaz/.venv/bin/gunicorn app:app --bind 127.0.0.1:8000 --workers 3
   ```
   Example unit file:
   ```
   [Service]
   WorkingDirectory=/opt/chumpitaz
   ExecStart=/opt/chumpitaz/.venv/bin/gunicorn app:app --bind 127.0.0.1:8000 --workers 3
   Restart=always
   User=www-data

   [Install]
   WantedBy=multi-user.target
   ```
4. Nginx config (serves built assets directly, proxies API, and forwards `/modelzoo/*` to the hosted demo):
   ```
   server {
       server_name www.chumpitaz.com;  # change to your domain
       root /opt/chumpitaz/frontend/dist;

       location /process_number {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       # Frontend link points to /modelzoo; proxy it to the hosted demo.
       location /modelzoo/ {
           proxy_pass https://modelzoo.app/;
           proxy_set_header Host modelzoo.app;
       }

       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```
   Reload Nginx after changes: `sudo nginx -s reload`.

### Deploy checklist
- `npm run build` before every deploy so `frontend/dist` is fresh.
- Ensure `modelzoo/mymodel` exists on the server (PyTorch weights).
- If you move the site to a new domain, update the Nginx `server_name` and DNS.
