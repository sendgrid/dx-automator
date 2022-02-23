from enum import Enum
from typing import List, Optional

import requests

COMPONENT_MEASURES_URL = 'https://sonarcloud.io/api/measures/component'


class Metrics(str, Enum):
    BRANCH_COVERAGE = 'branch_coverage'
    LINES_TO_COVER = 'lines_to_cover'
    UNCOVERED_LINES = 'uncovered_lines'


class SonarCloudApi:
    def get_component_measures(self, org: str, repo: str, metric_keys: List[Metrics]) -> Optional[List[dict]]:
        params = {
            'component': f'{org}_{repo}',
            'metricKeys': ','.join(metric_keys),
        }

        response = requests.get(COMPONENT_MEASURES_URL, params)
        response = response.json()

        if 'errors' in response:
            print(response['errors'])
            return

        return response['component']['measures']
