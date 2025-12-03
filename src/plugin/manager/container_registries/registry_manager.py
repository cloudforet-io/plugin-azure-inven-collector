import logging

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.container_registries.container_registries_connector import (
    ContainerRegistriesConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager
from spaceone.inventory.plugin.collector.lib import *

_LOGGER = logging.getLogger("spaceone")


class ContainerRegistriesManager(AzureBaseManager):
    cloud_service_group = "ContainerRegistries"
    cloud_service_type = "Registry"
    service_code = "/Microsoft.ContainerRegistry/registries"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Container", "Registry"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-container-registries.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        container_registries_conn = ContainerRegistriesConnector(
            secret_data=secret_data
        )
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        subscription_raw = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_raw)

        if not isinstance(subscription_info, dict):
            _LOGGER.error(
                "[ContainerRegistries] invalid subscription_info. raw=%r",
                subscription_raw,
            )
            error_responses.append(
                make_error_response(
                    error=Exception("Invalid subscription info"),
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )
            )
            return cloud_services, error_responses

        for registry in container_registries_conn.list_registries():
            try:
                registry_dict = self.convert_nested_dictionary(registry)
                if not isinstance(registry_dict, dict):
                    _LOGGER.error(
                        "[ContainerRegistries] registry list item is not dict. raw=%r",
                        registry,
                    )
                    continue

                registry_id = registry_dict["id"]
                resource_group_name = self.get_resource_group_from_id(registry_id)
                registry_name = registry_dict["name"]

                registry_dict = self.convert_nested_dictionary(
                    container_registries_conn.get_registry(
                        resource_group_name, registry_name
                    )
                )

                if not isinstance(registry_dict, dict):
                    _LOGGER.error(
                        "[ContainerRegistries] registry dict is not dict. "
                        f"rg={resource_group_name}, name={registry_name}, raw={registry_dict}"
                    )
                    continue

                registry_dict.update(
                    {
                        "resource_group": resource_group_name,
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": registry_id},
                    }
                )

                self._set_settings_info(registry_dict)

                self._set_services_info(
                    container_registries_conn,
                    registry_dict,
                    resource_group_name,
                    registry_name,
                )

                self._set_repository_permissions_info(
                    container_registries_conn,
                    registry_dict,
                    resource_group_name,
                    registry_name,
                )

                registry_dict = self.update_tenant_id_from_secret_data(
                    registry_dict, secret_data
                )
                self.set_region_code(registry_dict["location"])

                cloud_services.append(
                    make_cloud_service(
                        name=registry_dict["name"],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=registry_dict,
                        account=registry_dict["subscription_id"],
                        region_code=registry_dict["location"],
                        reference=self.make_reference(registry_id),
                        tags=self.convert_tag_format(registry_dict.get("tags", {})),
                        data_format="dict",
                    )
                )
            except Exception as e:
                _LOGGER.error(
                    f"[create_cloud_service] Error {self.service_code} {e}",
                    exc_info=True,
                )
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses

    def _set_settings_info(self, registry_dict):
        if not isinstance(registry_dict, dict):
            _LOGGER.error(
                "[ContainerRegistries] _set_settings_info called with non-dict: %r",
                registry_dict,
            )
            return

        registry_dict["admin_user_enabled"] = registry_dict.get(
            "admin_user_enabled", False
        )

        identities = []
        if identity_info := registry_dict.get("identity"):
            identity_type = identity_info.get("type", "None")
            if "SystemAssigned" in identity_type:
                identities.append(
                    {
                        "name": f"{registry_dict.get('name')}-system",
                        "type": "SystemAssigned",
                        "resource_group": registry_dict.get("resource_group"),
                        "subscription_id": registry_dict.get("subscription_id"),
                    }
                )

            for ua_id in identity_info.get("user_assigned_identities", {}):
                try:
                    parts = ua_id.split("/")
                    identities.append(
                        {
                            "name": parts[-1],
                            "type": "UserAssigned",
                            "resource_group": parts[4],
                            "subscription_id": parts[2],
                        }
                    )
                except Exception:
                    identities.append({"name": ua_id, "type": "UserAssigned"})
        registry_dict["identities"] = identities

        registry_dict["private_endpoints"] = []  # Placeholder

        policies = registry_dict.get("policies", {})
        registry_dict["domain_name_label_scope"] = policies.get(
            "quarantine_policy", {}
        ).get("status", "Unsecured")
        registry_dict["soft_delete_enabled"] = (
            policies.get("retention_policy", {}).get("status", "disabled") == "enabled"
        )
        registry_dict.setdefault("role_assignment_mode", "RBAC_REGISTRY")

        registry_dict["locks"] = []  # Placeholder

    def _set_services_info(self, conn, registry_dict, rg, name):
        if not isinstance(registry_dict, dict):
            _LOGGER.error(
                "[ContainerRegistries] _set_services_info called with non-dict: %r",
                registry_dict,
            )
            return

        registry_dict["repositories"] = []

        webhooks = conn.list_webhooks(rg, name)
        registry_dict["webhooks"] = [
            self.convert_nested_dictionary(w) for w in webhooks
        ]

        replications = conn.list_replications(rg, name)
        registry_dict["replications"] = [
            self.convert_nested_dictionary(r) for r in replications
        ]

        tasks = conn.list_tasks(rg, name)
        registry_dict["tasks"] = [self.convert_nested_dictionary(t) for t in tasks]

        connected_registries = conn.list_connected_registries(rg, name)
        registry_dict["connected_registries"] = [
            self.convert_nested_dictionary(cr) for cr in connected_registries
        ]

        cache_rules = conn.list_cache_rules(rg, name)
        registry_dict["cache_rules"] = [
            self.convert_nested_dictionary(rule) for rule in cache_rules
        ]
        registry_dict["cache_credentials"] = []

    def _set_repository_permissions_info(self, conn, registry_dict, rg, name):
        if not isinstance(registry_dict, dict):
            _LOGGER.error(
                "[ContainerRegistries] _set_repository_permissions_info called with non-dict: %r",
                registry_dict,
            )
            return

        tokens = conn.list_tokens(rg, name)
        token_list = []
        for t in tokens:
            td = self.convert_nested_dictionary(t)

            if not isinstance(td, dict):
                _LOGGER.error(
                    "[ContainerRegistries] token item is not dict. raw=%r",
                    t,
                )
                continue

            if creds := td.get("credentials"):
                td["password1_expiry"] = creds.get("password1", {}).get("expiry")
                td["password2_expiry"] = creds.get("password2", {}).get("expiry")
            token_list.append(td)
        registry_dict["tokens"] = token_list

        scope_maps = conn.list_scope_maps(rg, name)
        registry_dict["scope_maps"] = [
            self.convert_nested_dictionary(s) for s in scope_maps
        ]
