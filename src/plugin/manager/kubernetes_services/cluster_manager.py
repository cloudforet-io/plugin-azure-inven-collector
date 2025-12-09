import logging

from spaceone.inventory.plugin.collector.lib import *
from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.kubernetes_services.container_service_conector import (
    ContainerServiceConnector,
)
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class KubernetesServiceClusterManager(AzureBaseManager):
    cloud_service_group = "KubernetesService"
    cloud_service_type = "Cluster"
    service_code = "Microsoft.ContainerService/ManagedClusters"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Kubernetes", "AKS"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-kubernetes-services.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        cloud_services = []
        error_responses = []

        cs_conn = ContainerServiceConnector(secret_data=secret_data)
        sub_conn = SubscriptionsConnector(secret_data=secret_data)

        sub_raw = sub_conn.get_subscription(secret_data["subscription_id"])
        sub_info = self.convert_nested_dictionary(sub_raw)

        try:
            clusters = cs_conn.list_managed_cluster()
        except Exception as e:
            _LOGGER.error(
                f"[KubernetesServiceClusterManager] list_managed_cluster error: {e}",
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

        for cluster in clusters:
            try:
                cluster_dict = self.convert_nested_dictionary(cluster)
                resource_id = cluster_dict.get("id")
                resource_group = self.get_resource_group_from_id(resource_id)
                location = (cluster_dict.get("location") or "").replace(" ", "").lower()

                cluster_dict["resource_group"] = resource_group
                cluster_dict["subscription_id"] = sub_info["subscription_id"]
                cluster_dict["subscription_name"] = sub_info["display_name"]
                cluster_dict["location"] = location

                power_state = cluster_dict.get("power_state") or {}
                cluster_dict["power_state_display"] = power_state.get("code")

                fleet = cluster_dict.get("fleet") or {}
                fleet_id = fleet.get("id")
                cluster_dict["fleet_manager"] = (
                    fleet.get("name") or (fleet_id.split("/")[-1] if fleet_id else None)
                )

                # Node pools  (Target nodes / Ready nodes / OS ...)
                node_pools = []

                for pool in cluster_dict.get("agent_pool_profiles") or []:
                    auto_scaling = pool.get("enable_auto_scaling")

                    power_state = (pool.get("power_state") or {}).get("code")
                    min_count = pool.get("min_count")
                    max_count = pool.get("max_count")

                    ###TODO: target_nodes calculation is not fully accurate yet and will be improved in a future update.
                    # power_state = (pool.get("power_state") or {}).get("code")
                    # current_count = pool.get("count")
                    # min_count = pool.get("min_count")
                    # max_count = pool.get("max_count")
                    #
                    # # If the status is Stopped, the actual target is considered to be 0 (based on the portal Target node count).
                    # if isinstance(power_state, str) and power_state.lower() == "stopped":
                    #     target_nodes = 0
                    # else:
                    #     target_nodes = current_count

                    node_pools.append(
                        {
                            "node_pool": pool.get("name"),
                            "provisioning_state": pool.get("provisioning_state"),
                            "power_state": power_state,
                            "scale_method": "Autoscale" if auto_scaling else "Manual",
                            ###TODO: target_nodes calculation is not fully accurate yet and will be improved in a future update.
                            # "target_nodes": target_nodes,
                            "min_nodes": min_count,
                            "max_nodes": max_count,
                            "autoscaling_status": "Enabled" if auto_scaling else "Disabled",
                            "mode": pool.get("mode"),
                            "operating_system": pool.get("os_type"),
                        }
                    )

                cluster_dict["node_pools"] = node_pools

                # Security configuration
                oidc_profile = cluster_dict.get("oidc_issuer_profile") or {}
                security_profile = cluster_dict.get("security_profile") or {}
                aad_profile = cluster_dict.get("aad_profile") or {}
                addon_profiles = cluster_dict.get("addon_profiles") or {}

                image_cleaner = security_profile.get("image_cleaner") or {}
                interval_hours = image_cleaner.get("interval_hours")

                auth_mode = "Local accounts with Kubernetes RBAC"
                if aad_profile.get("managed"):
                    if aad_profile.get("enable_azure_rbac"):
                        auth_mode = "Microsoft Entra ID authentication with Azure RBAC"
                    else:
                        auth_mode = "Microsoft Entra ID authentication with Kubernetes RBAC"

                secret_store_addon = addon_profiles.get("azureKeyvaultSecretsProvider") or {}

                cluster_dict["security_configuration"] = {
                    "enable_oidc": oidc_profile.get("enabled"),
                    "issuer_url": oidc_profile.get("issuer_url"),
                    "enable_workload_identity": (
                        (security_profile.get("workload_identity") or {}).get("enabled")
                    ),
                    "enable_image_cleaner": image_cleaner.get("enabled"),
                    "scan_time_in_days": (
                        interval_hours / 24 if isinstance(interval_hours, (int, float)) else None
                    ),
                    "authentication": auth_mode,
                    "enable_secret_store_csi_driver": secret_store_addon.get("enabled"),
                }

                # Networking (Authorized IP ranges, VNet/Subnet, Cilium, Ingress …)
                net_profile = cluster_dict.get("network_profile") or {}
                api_profile = cluster_dict.get("api_server_access_profile") or {}

                pod_cidr = net_profile.get("pod_cidr") or ", ".join(
                    net_profile.get("podCidrs", []) or []
                )
                svc_cidr = net_profile.get("service_cidr") or ", ".join(
                    net_profile.get("serviceCidrs", []) or []
                )

                ###TODO:  VNet/Subnet: Search in the order of network_profile → agent_pool_profiles
                # vnet_subnet_id = (
                #     net_profile.get("vnet_subnet_id")
                #     or net_profile.get("vnetSubnetID")
                # )
                # if not vnet_subnet_id:
                #     for pool in (cluster_dict.get("agent_pool_profiles") or []):
                #         vnet_subnet_id = (
                #             pool.get("vnet_subnet_id") or pool.get("vnetSubnetID")
                #         )
                #         if vnet_subnet_id:
                #             break
                #
                # vnet_name = subnet_name = None
                # if vnet_subnet_id and "/subnets/" in vnet_subnet_id:
                #     vnet_part, subnet_part = vnet_subnet_id.split("/subnets/")
                #     vnet_name = vnet_part.split("/")[-1]
                #     subnet_name = subnet_part

                # Public / Private access
                public_access = (
                    "Disabled" if api_profile.get("enable_private_cluster") else "Enabled"
                )

                # Authorized IP ranges: If not, "Not enabled"
                auth_ip_ranges = api_profile.get("authorized_ip_ranges") or []
                if auth_ip_ranges:
                    authorized_ip_ranges = ", ".join(auth_ip_ranges)
                else:
                    authorized_ip_ranges = "Not enabled"

                # Ingress controller: based on addon state, if not present, "Not enabled"
                ingress_addon = (
                    addon_profiles.get("ingressApplicationGateway")
                    or addon_profiles.get("httpApplicationRouting")
                    or {}
                )
                if ingress_addon.get("enabled"):
                    ingress_controller = "Enabled"
                else:
                    ingress_controller = "Not enabled"

                # Cilium dataplane: "Not enabled" if no value is present
                data_plane_raw = str(net_profile.get("network_dataplane") or "")
                if data_plane_raw.lower() == "cilium":
                    cilium_dataplane = "Enabled"
                else:
                    cilium_dataplane = "Not enabled"

                cluster_dict["networking"] = {
                    "network_configuration": net_profile.get("network_plugin"),
                    "outbound_type": net_profile.get("outbound_type"),
                    "pod_cidr": pod_cidr,
                    "service_cidr": svc_cidr,
                    "dns_service_ip": net_profile.get("dns_service_ip"),
                    "cilium_dataplane": cilium_dataplane,
                    "network_policy_engine": net_profile.get("network_policy"),
                    "public_access_to_api_server": public_access,
                    "authorized_ip_ranges": authorized_ip_ranges,
                    "load_balancer": net_profile.get("load_balancer_sku"),
                ###TODO:  VNet/Subnet: Search in the order of network_profile → agent_pool_profiles
                    # "virtual_network": vnet_name,
                    # "subnet": subnet_name,
                    "ingress_controller": ingress_controller,
                }

                # Properties
                oms = addon_profiles.get("omsagent") or {}
                oms_config = oms.get("config") or {}
                http_routing = addon_profiles.get("httpApplicationRouting") or {}
                http_cfg = http_routing.get("config") or {}

                # Encryption type
                raw_enc_type = (security_profile.get("encryption") or {}).get(
                    "type"
                ) or security_profile.get("encryption_type")
                if raw_enc_type:
                    encryption_type = raw_enc_type
                else:
                    encryption_type = "Encryption at rest with platform-managed key"

                ###TODO: Workspace resource ID
                # workspace_resource_id = (
                #         oms_config.get("logAnalyticsWorkspaceResourceID")
                #         or oms_config.get("logAnalyticsWorkspaceResourceId")
                # )

                api_server_address = (
                        cluster_dict.get("fqdn")
                        or (api_profile.get("private_fqdn") if api_profile else None)
                )

                cluster_dict["properties_section"] = {
                    "kubernetes_version": cluster_dict.get("kubernetes_version"),
                    "dns_prefix": cluster_dict.get("dns_prefix"),
                    "api_server_address": api_server_address,
                    "rbac": "Enabled" if cluster_dict.get("enable_rbac") else "Disabled",
                    "encryption_type": encryption_type,
                    ###TODO: Workspace resource ID
                    # "workspace_resource_id": workspace_resource_id,
                    "infrastructure_resource_group": cluster_dict.get("node_resource_group"),
                    "http_application_routing_domain": http_cfg.get("HTTPApplicationRoutingZoneName"),
                    "resource_id": resource_id,
                    "location": location,
                    "resource_group": resource_group,
                    "subscription_id": sub_info["subscription_id"],
                }

                # Locks
                locks_raw = cs_conn.list_locks(resource_id)
                locks_list = []
                for lock in locks_raw:
                    lock_dict = self.convert_nested_dictionary(lock)
                    props = lock_dict.get("properties") or {}
                    lock_id = lock_dict.get("id", "")
                    scope = lock_id.split(
                        "/providers/Microsoft.Authorization/locks"
                    )[0]
                    locks_list.append(
                        {
                            "lock_name": lock_dict.get("name"),
                            "lock_type": props.get("level"),
                            "scope": scope,
                            "notes": props.get("notes"),
                        }
                    )
                cluster_dict["locks"] = locks_list

                # Common
                cluster_dict = self.update_tenant_id_from_secret_data(
                    cluster_dict, secret_data
                )
                self.set_region_code(location)

                cloud_services.append(
                    make_cloud_service(
                        name=cluster_dict.get("name"),
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=cluster_dict,
                        account=sub_info["subscription_id"],
                        region_code=location,
                        reference=self.make_reference(resource_id),
                        tags=self.convert_tag_format(cluster_dict.get("tags", {})),
                        data_format="dict",
                    )
                )

            except Exception as e:
                _LOGGER.error(
                    f"[KubernetesServiceClusterManager.create_cloud_service] Error: {e}",
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