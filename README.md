# The Developer Experience (DX) Automator

This tool is intended to help make managing multiple Github repositories much easier for DX, DevRel, and Open Source Engineering teams.

We will deploy the code to pypi once the MVP is ready. Thank you for your support!

# Announcements

**NEW:** If you're a software engineer who is passionate about #DeveloperExperience and/or #OpenSource, [this is an incredible opportunity to join our #DX team](https://sendgrid.com/careers/role/1421152/?gh_jid=1421152) as a Developer Experience Engineer and work with [@thinkingserious](https://github.com/thinkingserious) and [@aroach](https://github.com/aroach)! Tell your friends :)

## Contributing
Everyone who participates in our repo is expected to comply with our [Code of Conduct](https://github.com/sendgrid/dx-automator/blob/development/CODE_OF_CONDUCT.md).

We welcome [contributions](https://github.com/sendgrid/dx-automator/blob/development/CONTRIBUTING.md) in the form of issues, pull requests and code reviews. Or you can simply shoot us an [email](mailto:dx@sendgrid.com).

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

Start:

```bash
source ./init.sh
```

Run these commands to test if everything is working correctly.

```bash
curl http://$DX_IP/tasks/ping/pong
curl http://$DX_IP/tasks
curl http://$DX_IP/users/ping
curl http://$DX_IP/users
curl http://$DX_IP/github/ping
curl http://$DX_IP/github/members // must have the proper authorization
curl http://$DX_IP/github/is_member/<github_username> // check if a paricular GitHub username is part of your GitHub organization
curl --globoff "http://$DX_IP/github/items?repo=<repo_name>&issue_type=<issues or pull_requests>&labels[]=<label 1>?labels[]=<label 2>&states[]=<state 1>&states[]=<state 2>&limits[]=first&limits[]=100"
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

#### Get a List of the Top 20 Issues or PRs

```bash
source scripts/init-task-db 
python examples/update_rice_scores.py
python examples/rice_sorted_list_of_issues_and_prs.py
```

#### Restart a Particular Service

```bash
docker-compose -f docker-compose-dev.yml restart <Name of Service>
```

#### Run a Particular Test within a Python Service

```bash
docker-compose -f docker-compose-dev.yml run <service> python3 -m unittest <path.to.test>
```

For example

```bash
docker-compose -f docker-compose-dev.yml run tasks python3 -m unittest project.tests.test_tasks
```

#### Update the Hacktoberfest leaderboard

```bash
curl http://$DX_IP/hacktoberfest/leaders/update
```

#### Populate the local DB with all open GitHub issues and PRs

Note that by running this script a backup will be created with a file format of `tasks-db-backup.[current time stamp]`.

```bash
./scripts/init-task-db
docker-compose -f docker-compose-dev.yml exec tasks-db psql -U postgres
# \c tasks_dev
# select * from tasks;
# \q
```

### Examples

#### Retrieve all open and unlabeled issues

```bash
python ./examples/unlabled_issues.py
```

#### Retrieve all open issues that are bugs

```bash
python ./examples/open_security_issues.py
```

#### Retrieve all open issues that are security related

```bash
python ./examples/open_bugs.py
```

#### Retrieve all open issues that need a follow up response

```bash
python ./examples/follow_up.py
```

#### Retrieve all open prs that need a code review
```bash
python ./examples/code_review.py
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
