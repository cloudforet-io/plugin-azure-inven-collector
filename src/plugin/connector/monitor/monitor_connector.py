import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class MonitorConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_diagnostic_settings(self, resource_uri):
        return self.monitor_client.diagnostic_settings.list(resource_uri=resource_uri)

    def list_metrics(self, resource_uri, metricnames, aggregation, timespan=None, interval=None):
        return self.monitor_client.metrics.list(resource_uri, metricnames=metricnames, aggregation=aggregation,
                                                timespan=timespan, interval=interval)
