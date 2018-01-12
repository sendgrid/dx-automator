![SendGrid Logo](https://uiux.s3.amazonaws.com/2016-logos/email-logo%402x.png)

[![Travis Badge](https://travis-ci.org/sendgrid/dx-automator.svg?branch=develop)](https://travis-ci.org/sendgrid/dx-automator)

# The Developer Experience Automator

This tool was built by [@thinkingserious](https://www.twitter.com/thinkingserious) and [@mbernier](https://www.twitter.com/mbernier) at [SendGrid](https://www.sendgrid.com?source=dx-automator) in order to help scale the Developer Experience Team. We needed to spend less time tracking every single data point so that we could spend more time with our community. 

Since 2015, we have learned that the methods (FIFO and/or gut-based-prioritization) we were using to manage the work we need to do would not work with our small team or for our open source community.

[Intercom's RICE formula for prioritization](https://blog.intercom.com/rice-simple-prioritization-for-product-managers/) totally changed our workflow. We implemented this as our prioritization scheme for or backlog within a Google Doc and it served us very well until [Hacktoberfest 2017](https://sendgrid.com/blog/hacktoberfest-2017-was-amazing/). All of a sudden, our "magic spreadsheet" fell over. Our automations were not keeping up and we were spending as much time manually pushing GitHub Webhooks as we were manipulating our spreadsheet and merging pull requests. It was a mess. 

We found pain points with our spreadsheet, our automations, and our backlog. This project is the culmination of what we learned over the past couple years and it is helping us to be sgnificantly more effective.

## What this tool does

This tool connects actions on GitHub to a priority based kanban to-do list. 

The priorities are calculated using [RICE](https://blog.intercom.com/rice-simple-prioritization-for-product-managers/) as well as other possible controls, that are completely customizable by the user or team. For example, we use due dates and item status to effect the prioritization calculation.

The tool also allows you to set rules for what happens when specific actions are triggered. One of the default actions that is setup in the tool is to create an item from a pull request. From the pull request trigger, you could also set the automator to post a comment to the pull request with a thank you message, check whether a CLA needs to be signed, send an email, or any other number of actions. 

Another example would be a comment trigger on a task marked as "Waiting for feedback". If a comment comes in, and the task was waiting for feedback, the status could be updated to "Feedback received" which should bump the task up in priority.

Ultimately, the hope is to build multiple plugins, similar to the GitHub plugin. These plugins will add actions that can be used when triggers happen. This will allow the automator to do more of the menial work and allow teams to spend more time directly on coding or working with their community.

## Getting the Tool
To get the basic tool and all the plugins you can use:
```
git clone https://github.com/sendgrid/dx-automator .
```

## Installation
This project is built on Python, flask, and PostgreSQL. It can be deployed as a Docker Container or on a standalone server. 

### Docker Install

Clone the repo
```bash
git clone https://github.com/sendgrid/dx-automator.git
cd dx-automator
```

Create the docker machine
```bash
docker-machine create -d virtualbox dx
eval "$(docker-machine env dx)"
```

Build the docker container
```bash
docker-compose build
docker-compose up -d
```

Get the IP of your docker container and curl to make sure it's running
```
DX_IP="$(docker-machine ip dx)"
curl http://$DX_IP:5001/ping
```

Set up the database
```bash
docker-compose run dx-service python3 manage.py recreate_db
docker-compose run dx-service python3 manage.py seed_db
```

Validate that the items are seeded into the database
```bash
curl http://$DX_IP:5001/items
```

Run the tests to make sure everything is working! 
```bash
docker-compose run dx-service python3 manage.py test
```

### Your Server or On your machine

Clone the repo
```bash
git clone https://github.com/sendgrid/dx-automator.git
cd dx-automator
```

Create a virtual environment and activate it
```bash
python3.6 -m venv env
source env/bin/activate
```

Install the python dependencies
```bash
pip install -r requirements.txt
```

Set up the database and seed it
```bash
python manage.py recreate_db
python manage.py seed_db
```

Start up the flask server and get your IP
```bash
python manage.py runserver
```

Go to http://Your_IP:5001/items in your browser or via curl to verify the items in the database
```bash
curl http://$DX_IP:5001/items
```

Run the tests to make sure everything is working! 
```bash
python manage.py test
```

## Troubleshooting
For any issue, comment, or suggestion - please make an issue in the [GitHub repo](https://github.com/sendgrid/dx-automator). We want everything out in the open, so that if someone finds the same issue they can find the answer easily! This also makes it easy for us to track all our conversations. Yes, we have this system hooked up to this repo!

### Docker Machine is not working properly
If you have already installed and can't get the eval statement to work, try this to restart your machine:
```bash
docker-machine start dx
```

Then try from this step from install again:
```bash
eval "$(docker-machine env dx)"
```

## Contributing
Everyone who participates in our repo is expected to comply with our [Code of Conduct](./CODE_OF_CONDUCT).

We welcome [contributions](./CONTRIBUTING.md) in the form of issues, pull requests and code reviews. Or you can simply shoot us an [email](mailto:dx@sendgrid.com).

## Attributions
We believe in open source and want to give credit where it's due. We used the amazing tutorial at [testdriven.io](https://testdriven.io) to guide us in setting a solid foundation using flask, docker, and (eventually) node and react. From this tutorial, we began to build and iterate.
