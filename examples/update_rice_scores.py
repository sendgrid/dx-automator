# Reference: https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
from python_http_client import Client
import os
import json
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

client = Client(host="http://{}".format(os.environ.get('DX_IP')))

def get_repo_name(url):
    split = url.rsplit('/',3)
    return split[1]

def calculate_rice_reach(task):
    repo_to_reach_env_var = {
        'sendgrid-python': 'TWILIO_SENDGRID_PYTHON_REACH',
        'python-http-client': 'TWILIO_SENDGRID_PYTHON_REACH',
        'sendgrid-php': 'TWILIO_SENDGRID_PHP_REACH',
        'php-http-client': 'TWILIO_SENDGRID_PHP_REACH',
        'sendgrid-csharp': 'TWILIO_SENDGRID_CSHARP_REACH',
        'csharp-http-client': 'TWILIO_SENDGRID_CSHARP_REACH',
        'sendgrid-java': 'TWILIO_SENDGRID_JAVA_REACH',
        'java-http-client': 'TWILIO_SENDGRID_JAVA_REACH',
        'sendgrid-nodejs': 'TWILIO_SENDGRID_NODEJS_REACH',
        'nodejs-http-client': 'TWILIO_SENDGRID_NODEJS_REACH',
        'sendgrid-ruby': 'TWILIO_SENDGRID_RUBY_REACH',
        'ruby-http-client': 'TWILIO_SENDGRID_RUBY_REACH',
        'sendgrid-go': 'TWILIO_SENDGRID_GO_REACH',
        'rest': 'TWILIO_SENDGRID_GO_REACH'
    }
    reach_env_var = repo_to_reach_env_var.get(get_repo_name(task['url']), 'MAXIMUM_REACH')
    rice_reach = os.getenv(reach_env_var) or 0
    return float(rice_reach) + task['num_of_comments'] + task['num_of_reactions']

def calculate_rice_impact(task):
    if task['labels']:
        rice_impact = 1000
        if 'type: docs update' in task['labels']:
            rice_impact = 1
        if 'type: security' in task['labels']:
            rice_impact = 3
        if 'type: bug' in task['labels']:
            rice_impact = 3
        if 'type: twilio enhancement' in task['labels']:
            rice_impact = 2
        if 'type: sendgrid enhancement' in task['labels']:
            rice_impact = 2
        if 'type: community enhancement' in task['labels']:
            rice_impact = 1
        if 'type: getting started' in task['labels']:
            rice_impact = 2
        if 'type: question' in task['labels']:
            rice_impact = 1
        if task['task_type'] == 'pr':
            rice_impact = rice_impact + 1
        return rice_impact
    else:
        # This is unlabeled, we artificially inflate the
        # score in this case to ensure it's at the top to be processed first
        return 1000

def calculate_rice_confidence(task):
    rice_confidence = 1
    if task['language'] == 'go':
        rice_confidence = .8
    return rice_confidence

def calculate_rice_effort(task):
    if task['labels']:
        rice_effort = 0.0001
        if 'difficulty: easy' in task['labels']:
            rice_effort = 1
        if 'difficulty: medium' in task['labels']:
            rice_effort = 3
        if 'difficulty: hard' in task['labels']:
            rice_effort = 5
        if 'difficulty: very hard' in task['labels']:
            rice_effort = 8
        if 'difficulty: unknown or n/a' in task['labels']:
            rice_effort = .0001
        return rice_effort
    else:
        # This is unlabeled, we artificially inflate the
        # score in this case to ensure it's at the top to be processed first
        return .0001
    return rice_effort

def http_timestamp_to_datetime(http_timestamp):
    timestamp = mktime_tz(parsedate_tz(http_timestamp))
    return datetime.utcfromtimestamp(timestamp)

def needs_updating(task_id):
    task = get_task(task_id)
    if not task['updated_locally_at']:
        return True
    updated_at = http_timestamp_to_datetime(task['updated_at'])
    updated_locally_at = http_timestamp_to_datetime(task['updated_locally_at'])
    if updated_at > updated_locally_at:
        return True
    return False

def get_task(task_id):
    response = client.tasks._(task_id).get()
    task = json.loads(response.body)
    return task['message']

def get_tasks():
    response = client.tasks.get()
    tasks = json.loads(response.body)
    return tasks['message']['tasks']

def update_rice_score(task_id):
    if needs_updating(task_id):
        query_params = {
            "reach": calculate_rice_reach(task),
            "impact": calculate_rice_impact(task),
            "confidence": calculate_rice_confidence(task),
            "effort": calculate_rice_effort(task)
        }
        response = client.tasks.rice._(task_id).get(query_params=query_params)
        items = json.loads(response.body)
        return items
    return None

tasks = get_tasks()
for task in tasks:
    update_rice_score(int(task["id"]))

