# Deployment Guide

This guide explains how to run the **loven** Streamlit dashboard on your local machine, on a cloud PaaS, or a self-hosted VPS.

---

## 1. Local development (no Docker)

```bash
# Install loven with Streamlit and visualisation extras
pip install -e ".[viz]"
pip install streamlit openpyxl

# Launch the dashboard
streamlit run app/streamlit_app.py
```

The dashboard will open automatically at [http://localhost:8501](http://localhost:8501).

---

## 2. Docker (one-command setup)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 24 or Docker Engine + Docker Compose plugin

### Build and start

```bash
docker compose up --build
```

The dashboard will be available at [http://localhost:8501](http://localhost:8501).

The disk cache is persisted in a Docker volume (`loven_cache`) so cached
API responses survive container restarts.

### Stop

```bash
docker compose down
```

To also remove the cache volume:

```bash
docker compose down -v
```

---

## 3. Render (free tier)

[Render](https://render.com) can deploy a Docker container for free.

1. Push your repository to GitHub.
2. In the Render dashboard, click **New → Web Service**.
3. Select your repository and choose **Docker** as the environment.
4. Set the following:
   - **Port**: `8501`
   - **Health check path**: `/_stcore/health`
5. Click **Deploy**.

Render will build from the `Dockerfile` and expose the service on a public URL.

---

## 4. Railway

[Railway](https://railway.app) can deploy directly from a GitHub repository.

1. Create a new project and link your repository.
2. Railway auto-detects the `Dockerfile`.
3. In **Settings → Networking**, expose port `8501`.
4. Your dashboard is live at the generated Railway URL.

---

## 5. VPS / self-hosted

On any Ubuntu/Debian server with Docker installed:

```bash
# Clone the repository
git clone https://github.com/GizzZmo/loven.git
cd loven

# Start in the background
docker compose up -d --build

# View logs
docker compose logs -f
```

### Reverse proxy with nginx

```nginx
server {
    listen 80;
    server_name your.domain.com;

    location / {
        proxy_pass         http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
    }
}
```

Add HTTPS with [Certbot](https://certbot.eff.org/):

```bash
sudo certbot --nginx -d your.domain.com
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LOVDATA_BASE_URL` | `https://api.lovdata.no` | Override the Lovdata API endpoint |
| `PYTHONUNBUFFERED` | `1` | Ensure logs appear immediately |

Set environment variables in `docker-compose.yml` under the `environment:` key,
or export them before running `streamlit run`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install streamlit` |
| `ModuleNotFoundError: matplotlib` | Run `pip install 'loven[viz]'` |
| Port 8501 already in use | Change the host port in `docker-compose.yml` (e.g. `"8502:8501"`) |
| API timeout errors | Check your internet connection or use the sample data with `--base-url` |
