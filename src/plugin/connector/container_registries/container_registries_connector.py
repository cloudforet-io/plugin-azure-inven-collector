import logging

from plugin.connector.base import AzureBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ContainerRegistriesConnector(AzureBaseConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get("secret_data"))

    def list_registries(self):
        return self.container_registry_client.registries.list()

    def get_registry(self, resource_group_name, registry_name):
        return self.container_registry_client.registries.get(
            resource_group_name=resource_group_name, registry_name=registry_name
        )

    def list_webhooks(self, resource_group_name, registry_name):
        try:
            return self.container_registry_client.webhooks.list(
                resource_group_name=resource_group_name, registry_name=registry_name
            )
        except Exception as e:
            _LOGGER.error(f"[list_webhooks] Error: {e}")
            return []

    def list_replications(self, resource_group_name, registry_name):
        try:
            return self.container_registry_client.replications.list(
                resource_group_name=resource_group_name, registry_name=registry_name
            )
        except Exception as e:
            _LOGGER.error(f"[list_replications] Error: {e}")
            return []

    def list_usages(self, resource_group_name, registry_name):
        try:
            return self.container_registry_client.registries.list_usages(
                resource_group_name=resource_group_name, registry_name=registry_name
            )
        except Exception as e:
            _LOGGER.error(f"[list_usages] Error: {e}")
            return None

    def list_tokens(self, resource_group_name, registry_name):
        try:
            tokens_ops = getattr(self.container_registry_client, "tokens", None)
            if tokens_ops:
                return tokens_ops.list(
                    resource_group_name=resource_group_name, registry_name=registry_name
                )
        except Exception as e:
            _LOGGER.error(f"[list_tokens] Error: {e}")
        return []

    def list_scope_maps(self, resource_group_name, registry_name):
        try:
            scope_maps_ops = getattr(self.container_registry_client, "scope_maps", None)
            if scope_maps_ops:
                return scope_maps_ops.list(
                    resource_group_name=resource_group_name, registry_name=registry_name
                )
        except Exception as e:
            _LOGGER.error(f"[list_scope_maps] Error: {e}")
        return []

    def list_cache_rules(self, resource_group_name, registry_name):
        try:
            cache_rules_ops = getattr(
                self.container_registry_client, "cache_rules", None
            )
            if cache_rules_ops:
                return cache_rules_ops.list(
                    resource_group_name=resource_group_name, registry_name=registry_name
                )
        except Exception as e:
            _LOGGER.error(f"[list_cache_rules] Error: {e}")
        return []

    def list_connected_registries(self, resource_group_name, registry_name):
        try:
            connected_ops = getattr(
                self.container_registry_client, "connected_registries", None
            )
            if connected_ops:
                return connected_ops.list(
                    resource_group_name=resource_group_name, registry_name=registry_name
                )
        except Exception as e:
            _LOGGER.error(f"[list_connected_registries] Error: {e}")
        return []

    def list_tasks(self, resource_group_name, registry_name):
        try:
            tasks_ops = getattr(self.container_registry_client, "tasks", None)
            if tasks_ops:
                return tasks_ops.list(
                    resource_group_name=resource_group_name, registry_name=registry_name
                )
        except Exception as e:
            _LOGGER.error(f"[list_tasks] Error: {e}")
        return []
