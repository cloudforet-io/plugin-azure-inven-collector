from spaceone.core.error import ERROR_BASE


class ERROR_REPOSITORY_BACKEND(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Repository backend has problem. ({host})'


class ERROR_DRIVER(ERROR_BASE):
    status_code = 'INTERNAL'
    message = '{message}'


class ERROR_NOT_INITIALIZED_EXCEPTION(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Collector is not initialized. Please call initialize() method before using it.'


class ERROR_CONNECTOR_INITIALIZE(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Connector is failed to initialized. Connector = {e}.'


class ERROR_CONNECTOR(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Connector is failed to connect. Connector = {e}.'


class ERROR_KEY_VAULTS(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'KeyVault manager is failed to get sub resources. Manager = {e}.'


class ERROR_KEY_VAULTS_PERMISSION(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'KeyVault secret and certification information is failed. Please check the permission.'


class ERROR_PARSE_ID_FROM_RESOURCE_GROUP(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Parse resource name from resource ID is failed. Please check the variation.'

