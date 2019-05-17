# Reference: https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
from python_http_client import Client
import os
import json
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

client = Client(host="http://{}".format(os.environ.get('DX_IP')))

def calculate_rice_reach(task):
    # Last updated May 2019
    # https://docs.google.com/spreadsheets/d/1wNImudaEewPijd9EcgsHiEXbermh4amyug-2tTfyOWQ/edit#gid=2047355119
    rice_reach = 0
    if task['language'] == 'python':
        rice_reach = 7744
    if task['language'] == 'php':
        rice_reach = 68589
    if task['language'] == 'csharp':
        rice_reach = 41890
    if task['language'] == 'java':
        rice_reach = 11963
    if task['language'] == 'nodejs':
        rice_reach = 19225
    if task['language'] == 'ruby':
        rice_reach = 16417
    if task['language'] == 'go':
        rice_reach = 1835
    if task['language'] == 'openapi':
        # Setting to largest number because this effects all libs
        rice_reach = 68589
    return rice_reach + task['num_of_comments'] + task['num_of_reactions']

def calculate_rice_impact(task):
    if task['labels']:
        rice_impact = 0
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
        rice_effort = 0
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
    updated_at = http_timestamp_to_datetime(task['updated_at'])
    updated_locally_at = http_timestamp_to_datetime(task['updated_locally_at'])
    if updated_at > updated_locally_at:
        return True
    return False

def get_task(task_id):
    response = client.tasks._(task_id).get()
    task = json.loads(response.body)
    task = task['data']
    return task

def get_rice_score(task_id):
    if needs_updating(task_id):
        task = get_task(task_id)
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

task_id = 1
result = get_rice_score(task_id)
if result: 
    print(f'The RICE score for task_id:{task_id} is {result["data"]["rice_total"]}')
else:
    print('No update needed.')



