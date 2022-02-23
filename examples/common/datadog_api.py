from typing import List

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_payload import MetricsPayload
from datadog_api_client.v1.model.series import Series


class DatadogApi:
    def submit_metrics(self, series: List[Series]) -> None:
        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            body = MetricsPayload(series)
            api_instance.submit_metrics(body)
