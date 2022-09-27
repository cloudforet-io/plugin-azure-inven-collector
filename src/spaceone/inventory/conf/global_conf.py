CONNECTORS = {
    'AzureConnector': {
        'backend': 'spaceone.inventory.libs.connector.AzureConnector',
    },
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ]
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}
