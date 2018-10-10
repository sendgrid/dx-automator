# The Developer Experience (DX) Automator

This tool is intended to help make managing multiple Github repositories much easier for DX, DevRel, and Open Source Engineering teams. 

Please check out the [development branch](https://github.com/sendgrid/dx-automator/tree/development) to see what's going on.

We will update this README and the master branch, as well as deploy the code to pypi once the MVP is ready!

## Contributing
Everyone who participates in our repo is expected to comply with our [Code of Conduct](./CODE_OF_CONDUCT).

We welcome [contributions](./CONTRIBUTING.md) in the form of issues, pull requests and code reviews. Or you can simply shoot us an [email](mailto:dx@sendgrid.com).//open

## Attributions
We believe in open source and want to give credit where it's due. We used the amazing tutorial at [testdriven.io](https://testdriven.io) to guide us in setting a solid foundation using flask, docker, and (eventually) node and react. From this tutorial, we began to build and iterate.

## Usage

### Create AWS Docker Machine

```bash
docker-machine create --driver amazonec2 dx-automator-prod
```

### Deploy to AWS

```bash
docker-machine env dx-automator-prod
eval $(docker-machine env dx-automator-prod)
docker-compose -f docker-compose-prod.yml up -d --build
DX_IP="$(docker-machine ip dx-automator-prod)"
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
```

### Create Local Docker Machine

```bash
docker-machine create -d virtualbox dx-automator-dev
```

### Deploy Locally

```bash
docker-machine start dx-automator-dev
docker-machine env dx-automator-dev
eval $(docker-machine env dx-automator-dev)
docker-compose -f docker-compose-dev.yml up -d --build
DX_IP="$(docker-machine ip dx-automator-dev)"
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
```

### Connect to Local DB

```bash
docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
# \c users_dev
# select * from users;
# \q
```
