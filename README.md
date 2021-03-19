# The Developer Experience (DX) Automator

This tool is intended to help make managing multiple Github repositories much easier for DX, DevRel, and Open Source Engineering teams.

We will deploy the code to pypi and create an initial release once the MVP is ready. Thank you for your support!

**The default branch name for this repository has been changed to `main` as of 07/23/2020.**

## Contributing
Everyone who participates in our repo is expected to comply with our [Code of Conduct](CODE_OF_CONDUCT.md).

We welcome [contributions](CONTRIBUTING.md) in the form of issues, pull requests and code reviews. Or you can simply shoot us an [email](mailto:dx@sendgrid.com).

## Attributions
We believe in open source and want to give credit where it's due. We used an amazing tutorial at [testdriven.io](https://testdriven.io) to guide us in setting up a solid foundation using flask, docker, and (eventually) node and react. This tutorial helped us build and iterate this project successfully!

## Prerequisites

* Virtual Box
* Docker

## Usage - Local

### Standalone Scripts

Some example scripts don't require a running Automator web server to execute (e.g., `action_items`, `metrics`, `opened_items`, `closed_items`). Use the steps below to run these scripts.

#### Environment Setup

Update the development environment with your [GITHUB_TOKEN](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line), for example:

1. Copy the sample environment file to a new file: `cp .env_sample .env`
1. Edit the new `.env` to add your GitHub Personal Access Token
1. Source the `.env` file to set the variable in the current session: `source .env`

Install the python dependencies and activate the environment:

```bash
make install
source venv/bin/activate
```

#### Running Scripts

```bash
python ./examples/action_items.py
python ./examples/metrics.py daily
python ./examples/metrics.py weekly
```

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

### Connect to a service's container and enter a Bash prompt

```bash
docker exec -it <container name> /bin/bash
```

### Admin Commands

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

#### Get a List of the Top 20 Issues or PRs

```bash
./scripts/init-task-db 
python3 examples/update_rice_scores.py
python3 examples/rice_sorted_list_of_issues_and_prs.py
```

#### Retrieve all open and unlabeled issues

```bash
python ./examples/unlabeled_issues.py
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

#### Retrieve a list of releases for each repo

```bash
python ./examples/releases.py
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
