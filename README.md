# Docker usage for this project

This project is packaged with Docker using the top-level `Dockerfile`.

## What this Dockerfile does

- `FROM python:3.11-slim`
  - Uses the official Python 3.11 base image.
  - Provides a minimal Linux environment with Python installed.
- `WORKDIR /app`
  - Sets the working directory inside the container to `/app`.
  - Docker creates `/app` automatically if it does not exist.
- `COPY requirements.txt .`
  - Copies only `requirements.txt` from the build context into `/app/requirements.txt`.
  - This helps Docker cache dependency installation separately from code changes.
- `RUN pip install --no-cache-dir -r requirements.txt`
  - Installs Python dependencies listed in `requirements.txt`.
- `COPY . .`
  - Copies the rest of the current project into the container.
  - This includes `app.py`, `game/`, `chatbot/`, and other files.
- `EXPOSE 8000`
  - Documents that the container listens on port 8000.
  - Does not publish the port by itself.
- `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]`
  - Runs the FastAPI app when the container starts.

## Build commands

If you want to run the Streamlit UI locally, install dependencies first:

```bash
pip install -r requirements.txt
```

### Build with a tag (recommended)

```bash
docker build -t my-first-app .
```

- `-t` sets the image name (tag). In this case, the image will be named `my-first-app`.
- This makes it easy to refer to the image later when running it.
- `.` means "use the current directory as the build context".

### Build without a tag

```bash
docker build .
```

- Docker builds the image and prints an image ID.
- The image will be harder to reference later because it has no friendly name.
- You can still run it using the image ID.

### Build with a version tag

```bash
docker build -t my-first-app:latest .
```

- `my-first-app:latest` adds a version label to the image.
- Common pattern: `name:version` or `name:latest`.

## Run commands

### Run the image by name

```bash
docker run -p 8000:8000 my-first-app
```

- `-p 8000:8000` publishes container port 8000 to host port 8000.
- Then you can access the app API at `http://localhost:8000`.

> When deploying to Cloud Run, the service provides `PORT=8080` automatically. The Dockerfile now reads `PORT` and falls back to `8000` for local development.

### Run in detached mode

```bash
docker run -d -p 8000:8000 my-first-app
```

- `-d` runs the container in the background.
- Use `docker ps` to see running containers.

### Run with an image ID

```bash
docker run -p 8000:8000 <image-id>
```

- Works if you built without `-t`.
- Use `docker images` to find the image ID.

### Run the Streamlit UI locally

```bash
streamlit run app.py
```

- This opens the UI in your browser.
- Use the Game and Chatbot tabs to interact with the project.
- The Chatbot will still require `GEMINI_API_KEY` in `.env`.

### Run the FastAPI server locally

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

- This starts the unified FastAPI backend on port 8000.
- The same `app.py` file now supports both API and Streamlit UI.

## Step-by-step: build and run the project

1. Open a terminal in the project root where `Dockerfile` and `requirements.txt` are located.
2. Build the image with a name:

```bash
docker build -t my-first-app .
```

3. Confirm the image exists:

```bash
docker images
```

4. Run the container, mapping host port `8000` to container port `8000`:

```bash
docker run -p 8000:8000 my-first-app
```

5. Open the app in your browser at:

```bash
http://localhost:8000
```

6. If you want the app on host port `8080`, use this port mapping instead:

```bash
docker run -p 8080:8000 my-first-app
```

Then open:

```bash
http://localhost:8080
```

7. To run the container in the background:

```bash
docker run -d -p 8000:8000 my-first-app
```

8. Check running containers:

```bash
docker ps
```

## Useful Docker commands

- List local images:

```bash
docker images
```

- List running containers:

```bash
docker ps
```

- List all containers:

```bash
docker ps -a
```

- Stop a running container:

```bash
docker stop <container-id>
```

- Remove a stopped container:

```bash
docker rm <container-id>
```

- Remove an image:

```bash
docker rmi my-first-app
```

## Push your image to Docker Hub

1. Create or log in to your Docker Hub account at https://hub.docker.com.
2. Create a Docker Hub access token (recommended):
   - Go to your profile menu > Account Settings > Security.
   - Click **New Access Token** and save the generated token.
3. Log in from the terminal:

```bash
docker login --username your-dockerhub-username
```

- When prompted, enter the access token as the password.
- You can also run `docker login` and enter the token instead of your password.

4. Tag your local image for Docker Hub:

```bash
docker tag my-first-app your-dockerhub-username/my-first-app:latest
```

5. Push the tagged image:

```bash
docker push your-dockerhub-username/my-first-app:latest
```

6. Verify the image is on Docker Hub by visiting:

```text
https://hub.docker.com/repository/docker/your-dockerhub-username/my-first-app
```

### Notes

- Docker Hub repository names must include your username or organization, e.g. `zangrajazz/my-first-app`.
- Pushing to `my-first-app` without the username attempts to use the `library/` namespace and will fail.
- If you need to logout, use:

```bash
docker logout
```

## Why copy `requirements.txt` separately?

This is a build performance optimization:

- If `requirements.txt` has not changed, Docker can reuse the cached layer after `pip install`.
- If you copy the entire project first and then install dependencies, any code change invalidates the previous cache.
- Copying dependencies first means only code changes trigger a rebuild of the later layer.

## What the container structure looks like

When built, the container will have the project under `/app`:

- `/app/app.py`
- `/app/Dockerfile`
- `/app/requirements.txt`
- `/app/game/`
- `/app/chatbot/`
- other project files

## Notes

- The `Dockerfile` is expected to be in the project root.
- Run the build command from the same folder where `Dockerfile` and `requirements.txt` are located.
- If you add or remove dependencies, update `requirements.txt` and rebuild the image.