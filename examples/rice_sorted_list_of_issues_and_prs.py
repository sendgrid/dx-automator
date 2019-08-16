import json

from common.automator_client import client

query_params = {
    "page_index": 1,
    "num_results": 20
}
response = client.tasks.rice.get(query_params=query_params)
responses = json.loads(response.body)['message']
for task in responses:
    print(f'{"{:.2f}".format(task["rice_total"]).ljust(10)}: "{task["title"]}": {task["url"]}')
