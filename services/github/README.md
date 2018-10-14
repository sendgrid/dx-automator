# Local Development Installation

### Create the Docker Machine

```bash
docker-machine create -d virtualbox dx-automator-github-dev
```

### Connect your Docker Client to the Docker Engine running on the virtual machine

```bash
eval "$(docker-machine env dx-automator-github-dev)"
```

### Setup the Environment Variables

```bash
mv .env_sample .env
```

### Update the variables in `.env`.

```bash
source .env
```

### Build the Docker Image and run the Docker Container in the Background

```bash
docker-compose -f docker-compose-dev.yml up -d --build
```

### Run the tests

Update the `test_users` in `project\tests\test_github.py`.

```bash
docker-compose -f docker-compose-dev.yml run github-service python manage.py test
```

### Get the IP of the Docker Machine

```bash
GITHUB_IP="$(docker-machine ip dx-automator-github-dev)"
```


# Deploy Production to Amazon

### Create the Docker Machine

```bash
docker-machine create --driver amazonec2 dx-automator-github-prod
```

### Activate the Deploy Machine

```bash
docker-machine env dx-automator-github-prod
eval $(docker-machine env dx-automator-github-prod)
```

### Setup the Environment Variables

```bash
mv .env_sample .env
```

### Update the variables in `.env`.

```bash
source .env
```

### Deploy Production

```bash
docker-compose -f docker-compose-prod.yml up -d --build
```

### Run the tests

Update the `test_users` in `project\tests\test_github.py`.

```bash
docker-compose -f docker-compose-prod.yml run github-service python manage.py test
```


# Reference

### Kill All the Running Docker Instances

```bash
docker stop $(docker ps -a -q)
```

### Check the Environment on the Server

```bash
docker-compose -f docker-compose-prod.yml run github-service env
```


# Usage

Check if a GitHub username belongs to the organization which is set in the `.env` file

```bash
curl http://$GITHUB_IP:5001/is_member/<github-username>
```
