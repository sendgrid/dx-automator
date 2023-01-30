from collections import namedtuple
from typing import Dict, List

Label = namedtuple('Label', 'name color description')

ALL_LABELS: List[Label] = [
    Label('code-generation', '8800ff', 'issue deals with generated code'),
    Label('dependencies', '0366d6', 'pull requests that update a dependency file'),
    Label('difficulty: easy', 'c2e0c6', 'fix is easy in difficulty'),
    Label('difficulty: medium', 'fef2c0', 'fix is medium in difficulty'),
    Label('difficulty: hard', 'f9d0c4', 'fix is hard in difficulty'),
    Label('difficulty: very hard', 'e99695', 'fix is very hard in difficulty'),
    Label('difficulty: unknown or n/a', 'ffffff', 'fix is unknown in difficulty'),
    Label('status: code review request', 'cccccc', 'requesting a community code review or review from Twilio'),
    Label('status: duplicate', 'cccccc', 'duplicate issue'),
    Label('status: help wanted', 'cccccc', 'requesting help from the community'),
    Label('status: invalid', 'cccccc', 'issues not related to the library'),
    Label('status: ready for deploy', 'cccccc', 'code ready to be released in next deploy'),
    Label('status: ready for merge', 'cccccc', 'code deemed fit for merge'),
    Label('status: waiting for feedback', 'cccccc', 'waiting for feedback from the submitter'),
    Label('status: wontfix', 'cccccc', 'enhancement or fix that was rejected'),
    Label('status: work in progress', 'cccccc', 'Twilio or the community is in the process of implementing'),
    Label('status: waiting for feature', 'cccccc', 'feature will be implemented in the future'),
    Label('type: getting started', '0e8a16', 'question while getting started'),
    Label('type: question', 'fbca04', 'question directed at the library'),
    Label('type: bug', 'b60205', 'bug in the library'),
    Label('type: docs update', '5319e7', 'documentation change not affecting the code'),
    Label('type: support', '006b75', 'ticket that should be redirected to support'),
    Label('type: non-library issue', '006b75', 'API issue not solvable via the SDK'),
    Label('type: community enhancement', '1d76db', 'feature request not on Twilio\'s roadmap'),
    Label('type: twilio enhancement', '0052cc', 'feature request on Twilio\'s roadmap'),
    Label('type: security', 'b60205', 'known security issue'),
    Label('stale', 'f0A286', 'The issue is older than 30 days and queued for being closed'),
    Label('triage queue', '006B75', 'Issue is in our internal backlog. It\'s either a bug or a feature enhancement.'),

]


def get_labels() -> Dict[str, Label]:
    labels = {}

    for label in ALL_LABELS:
        if label.name in labels:
            raise KeyError(f'Duplicate label name: {label}')

        labels[label.name] = label

    return labels
