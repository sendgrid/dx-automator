# Create Docker Machine

```bash
docker-machine create -d virtualbox dx-automator-github-dev
```

# Point the Docker Client to the Docker Machine

```bash
eval "$(docker-machine env dx-automator-github-dev)"
```

# Build the Docker Image

```bash
source .env
docker-compose build
```

# Re-Build the Docker Image

Needed when updating requirements.txt

```bash
source .env
docker-compose up -d --build
```

# Run the Docker Container in the Background

```bash
docker-compose up -d
```

# Get the IP of the Docker Machine

```bash
docker-machine ip dx-automator-github-dev
```

# Run Tests

```bash
docker-compose run github-service python manage.py test
```

# Create Deploy Machine

```bash
docker-machine create --driver amazonec2 dx-automator-github-prod
```

# Activate Deploy Machine

```bash
docker-machine env dx-automator-github-prod
eval $(docker-machine env dx-automator-github-prod)
docker-machine ls
```

# Kill All Running Docker Instances

```bash
docker stop $(docker ps -a -q)
```

# Deploy

```bash
source .env
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml run github-service python manage.py test
```

# Check Environment on Server

```bash
docker-compose -f docker-compose-prod.yml run github-service env
```

# USAGE

curl http://<YOUR IP>:5001/is_a_member/<username>