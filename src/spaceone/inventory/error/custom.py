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
    message = 'Connector is failed to initialized. Connector = {field}.'


class ERROR_CONNECTOR(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Connector is failed to connect. Connector = {field}.'


class ERROR_KEY_VAULTS(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'KeyVault manager is failed to get sub resources. {field}.'


class ERROR_KEY_VAULTS_PERMISSION(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'KeyVault secret and certification information is failed. Please check the permission.'


class ERROR_PARSE_ID_FROM_RESOURCE_GROUP(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Parse resource name from resource ID is failed. Please check the variation.'


class ERROR_MANAGER_GET_ADDITIONAL_RESOURCE_INFO(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Get an additional information of the resource is failed. Please check the variation. Manager = {field}'


class ERROR_GET_RESOURCE_NAME_FROM_ID(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Get resource name from id is failed. field = {e}.'


class ERROR_CONNECTOR_GET_ADDITIONAL_RESOURCE_INFO(ERROR_BASE):
    status_code = 'INTERNAL'
    message = 'Get an additional information of the resource is failed. Please check the variation. Connector = {field}'
