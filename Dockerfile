# ---- Base image -------------------------------------------------------------
# 'slim' = small Debian-based Python image. Smaller image = faster build/push/pull.
FROM python:3.12-slim

# Don't buffer stdout/stderr -> logs show up immediately in `docker logs`.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Everything below happens inside /app in the container.
WORKDIR /app

# ---- Dependencies first (layer caching) -------------------------------------
# Copy ONLY requirements first. Docker caches this layer, so if your code
# changes but deps don't, the slow `pip install` step is reused = fast builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- App code ---------------------------------------------------------------
COPY app ./app

# Document the port the app listens on (metadata; doesn't actually open it).
EXPOSE 8000

# ---- Start command ----------------------------------------------------------
# 0.0.0.0 (not 127.0.0.1) so the server is reachable from OUTSIDE the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
