# CI/CD POC — FastAPI + Docker

A minimal backend you'll wire into a real CI/CD pipeline. This step gets the app
running in a container **on your machine**. The GitHub Actions pipeline and
self-hosted runner come next.

## Files

| File | What it is |
|---|---|
| `app/main.py` | FastAPI app: `/health` + in-memory `/items` CRUD |
| `requirements.txt` | Python dependencies (pinned versions = reproducible builds) |
| `Dockerfile` | Recipe to build the app into a Docker image |
| `.dockerignore` | Keeps junk out of the image (like `.gitignore` for Docker) |

## Run it locally WITHOUT Docker (fastest sanity check)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs — FastAPI auto-generates an interactive API page.
Try `/health`, create an item with `POST /items`, list them with `GET /items`.

## Run it WITH Docker (this is what the pipeline will automate)

```bash
# 1. Build an image named 'cicd-poc' from the Dockerfile in this folder
docker build -t cicd-poc .

# 2. Run a container from that image, mapping YOUR port 8000 -> container's 8000
docker run --rm -p 8000:8000 cicd-poc
```

Now http://127.0.0.1:8000/docs works again — but served from inside a container.

Useful commands to know:

```bash
docker ps                 # list running containers
docker logs <container>   # view logs
docker stop <container>   # stop it
docker images             # list built images
```

### The `-p 8000:8000` bit matters

Left number = port on YOUR machine. Right = port INSIDE the container. The
container is a sealed box; this flag pokes one hole so you can reach the app.
Remember the wondering question about two deploys fighting over port 8000? This
flag is exactly where that fight happens.

## What the pipeline will do (so this manual step makes sense)

Everything you just typed by hand is what the robot will do automatically:

1. `docker build` — on a GitHub cloud runner, on every push
2. `docker push` — upload the image to `ghcr.io` (GitHub's registry)
3. `docker pull` + `docker run` — on your **self-hosted runner** (this machine)

Do it by hand once and the YAML in the next step reads like a to-do list you
already understand.

## Next steps

- [x] FastAPI app + Dockerfile (you are here)
- [ ] Push to a GitHub repo
- [ ] `.github/workflows/deploy.yml` — build + push to ghcr.io
- [ ] Install the self-hosted runner on this machine
- [ ] Add the deploy job → push a commit → watch it deploy itself
- [ ] Break something on purpose → practice a rollback
