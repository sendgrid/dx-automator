# DX Automator

## Create AWS Docker Machine

```bash
docker-machine create --driver amazonec2 dx-automator-prod
```

## Deploy to AWS

```bash
docker-machine env dx-automator-prod
eval $(docker-machine env dx-automator-prod)
docker-compose -f docker-compose-prod.yml up -d --build
DX_IP="$(docker-machine ip dx-automator-prod)"
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
```

## Create Local Docker Machine

```bash
docker-machine create -d virtualbox dx-automator-dev
```

## Deploy Locally

```bash
docker-machine start dx-automator-dev
docker-machine env dx-automator-dev
eval $(docker-machine env dx-automator-dev)
docker-compose -f docker-compose-dev.yml up -d --build
DX_IP="$(docker-machine ip dx-automator-dev)"
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
```

## Connect to Local DB

```bash
docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
# \c users_dev
# select * from users;
# \q
```

