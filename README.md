# The Developer Experience (DX) Automator

This tool is intended to help make managing multiple Github repositories much easier for DX, DevRel, and Open Source Engineering teams. 

We will deploy the code to pypi once the MVP is ready. Thank you for your support!

# Announcements

**NEW:** If you're a software engineer who is passionate about #DeveloperExperience and/or #OpenSource, [this is an incredible opportunity to join our #DX team](https://sendgrid.com/careers/role/1421152/?gh_jid=1421152) as a Developer Experience Engineer and work with [@thinkingserious](https://github.com/thinkingserious) and [@aroach](https://github.com/aroach)! Tell your friends :)

## Contributing

Everyone who participates in our repo is expected to comply with our [Code of Conduct](./CODE_OF_CONDUCT).

We welcome [contributions](./CONTRIBUTING.md) in the form of issues, pull requests and code reviews, or you can simply shoot us an [email](mailto:dx@sendgrid.com).

## Attributions
We believe in open source and want to give credit where it's due. We used an amazing tutorial at [testdriven.io](https://testdriven.io) to guide us in setting up a solid foundation using flask, docker, and (eventually) node and react. This tutorial helped us build and iterate this project successfully!

## Prerequisites

* Docker

## Usage - Local

### Create Local Docker Machine

```bash
docker-machine create -d virtualbox dx-automator-dev
```

### Deploy Locally

Setup your environment variables:

```bash
cp ./services/github/.env_sample ./services/github/.env
cp ./services/looker/.env_sample ./services/looker/.env
cp ./services/hacktoberfest/.env_sample ./services/hacktoberfest/.env
```

Install:

```bash
source ./init.sh
```

Run these commands to test if everything is working correctly.

```bash
curl http://$DX_IP/tasks/ping
curl http://$DX_IP/tasks
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
curl http://$DX_IP/github/ping
curl http://$DX_IP/github/members
curl http://$DX_IP/github/is_member/<github_username>
curl http://$DX_IP/github/prs?repo=<repo_name>
curl http://$DX_IP/github/issues?repo=<repo_name>
curl --globoff "http://$DX_IP/github/issues?repo=<repo_name>&labels=<label 1>&labels=<label 2>"
curl http://$DX_IP/looker/ping
curl http://$DX_IP/looker/4404
curl http://$DX_IP/hacktoberfest/ping
curl http://$DX_IP/hacktoberfest/sendgrid/leaders/2018
```

Grab the IP address.

```
echo $DX_IP
```

And now paste that IP into your browser and you should see a task list.

### Stop Local Containers and the Docker Machine

```bash
source ./stop.sh
```

### Stop Local Containers and Delete Images and the Docker Machine

```bash
source ./kill.sh
```

### Connect to the Local DB

```bash
docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
# \c users_dev
# select * from users;
# \q
```

### Admin Commands

```bash
curl http://$DX_IP/hacktoberfest/leaders/update
```

### Examples

#### Retrieve all open and unlabed issues

```bash
python ./examples/unlabled_issues.py
```

#### Retrieve all open issues that are bugs

```bash
python ./examples/open_bugs.py
```

#### Retrieve all open issues that need a follow up response

```bash
python ./examples/follow_up.py
```

## Usage - Cloud

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