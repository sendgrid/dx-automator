import re
from enum import Enum
from typing import Dict, List, Optional

import requests

PROJECT_BRANCHES_URL = 'https://sonarcloud.io/api/project_branches/list'
COMPONENT_MEASURES_URL = 'https://sonarcloud.io/api/measures/component'

PRE_RELEASE_BRANCH_REGEX = r'\d+\.0\.0-\w+'


class ProjectBranch:
    def __init__(self, branch_data: Dict[str, any]) -> None:
        self.branch_data = branch_data

        self.name = branch_data['name']
        self.is_main = branch_data['isMain']
        self.is_pre_release = re.match(PRE_RELEASE_BRANCH_REGEX, self.name) is not None

    def __repr__(self) -> str:
        return self.name


class Metrics(str, Enum):
    BRANCH_COVERAGE = 'branch_coverage'
    LINES_TO_COVER = 'lines_to_cover'
    UNCOVERED_LINES = 'uncovered_lines'


class SonarCloudApi:

    def get_project_branches(self, org: str, repo: str) -> Optional[List[ProjectBranch]]:
        params = {
            'project': f'{org}_{repo}',
        }

        response = requests.get(PROJECT_BRANCHES_URL, params)
        response = response.json()

        if 'errors' in response:
            print(response['errors'])
            return

        return [ProjectBranch(branch) for branch in response['branches']]

    def get_component_measures(self, org: str, repo: str, branch: str,
                               metric_keys: List[Metrics]) -> Optional[List[dict]]:
        params = {
            'component': f'{org}_{repo}',
            'branch': branch,
            'metricKeys': ','.join(metric_keys),
        }

        response = requests.get(COMPONENT_MEASURES_URL, params)
        response = response.json()

        if 'errors' in response:
            print(response['errors'])
            return

        return response['component']['measures']
