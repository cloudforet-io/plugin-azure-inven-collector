import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import ICON_URL
from plugin.connector.functions.functions_connector import FunctionsConnector
from plugin.connector.subscriptions.subscriptions_connector import (
    SubscriptionsConnector,
)
from plugin.manager.base import AzureBaseManager

_LOGGER = logging.getLogger("spaceone")


class FunctionsManager(AzureBaseManager):
    cloud_service_group = "Functions"
    cloud_service_type = "Instance"
    service_code = "/Microsoft.Web/sites"

    def create_cloud_service_type(self):
        return make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            service_code=self.service_code,
            metadata_path=self.get_metadata_path(),
            is_primary=True,
            is_major=True,
            labels=["Serverless"],
            tags={"spaceone:icon": f"{ICON_URL}/azure-functions.svg"},
        )

    def create_cloud_service(self, options, secret_data, schema):
        # Collect function apps
        cloud_services = []
        error_responses = []

        functions_conn = FunctionsConnector(secret_data=secret_data)
        subscription_conn = SubscriptionsConnector(secret_data=secret_data)

        # Load subscription info
        subscription_obj = subscription_conn.get_subscription(
            secret_data["subscription_id"]
        )
        subscription_info = self.convert_nested_dictionary(subscription_obj)

        # Fetch function app list
        try:
            function_app_list = functions_conn.list_function_apps()
        except Exception as e:
            _LOGGER.error("[FunctionsManager] list_function_apps error: %s", e, exc_info=True)
            error_responses.append(
                make_error_response(
                    error=e,
                    provider=self.provider,
                    cloud_service_group=self.cloud_service_group,
                    cloud_service_type=self.cloud_service_type,
                )
            )
            return cloud_services, error_responses

        # Iterate function apps
        for function_app in function_app_list:
            try:
                fa_dict = self.convert_nested_dictionary(function_app)
                resource_id = fa_dict.get("id")

                # Base fields
                resource_group = self.get_resource_group_from_id(resource_id)
                location = (fa_dict.get("location") or "").replace(" ", "").lower()
                fa_dict["location"] = location

                # Function app detail
                site_detail = functions_conn.get_function_app_detail(resource_id) or {}
                site_props = (site_detail.get("properties") or {})

                fa_dict["properties"] = site_props
                fa_dict["status"] = site_props.get("state")
                server_farm_id = site_props.get("serverFarmId")
                fa_dict["server_farm_id"] = server_farm_id

                # App Service Plan detail
                plan_detail = functions_conn.get_app_service_plan_detail(server_farm_id) or {} if server_farm_id else {}
                plan_sku = (plan_detail.get("sku") or {})
                plan_props = (plan_detail.get("properties") or {})

                sku_name = plan_sku.get("name")
                sku_tier = plan_sku.get("tier")
                pricing_tier = sku_tier or sku_name

                fa_dict["pricing_tier"] = pricing_tier
                fa_dict["sku"] = plan_sku

                # Plan metadata
                plan_name = plan_detail.get("name") or (server_farm_id.split("/")[-1] if server_farm_id else None)
                plan_rg = self.get_resource_group_from_id(server_farm_id) if server_farm_id else None
                plan_location = plan_detail.get("location") or location

                # Instance count
                instance_count = plan_props.get("numberOfWorkers") or plan_props.get("capacity")

                # Apps count (slots removed)
                apps_count = plan_props.get("numberOfSites")

                # OS detection
                reserved = plan_props.get("reserved")
                if reserved is True:
                    operating_system = "Linux"
                elif reserved is False:
                    operating_system = "Windows"
                else:
                    operating_system = None

                # Zone redundant
                zone_flag = plan_props.get("zoneRedundant")
                if zone_flag is True:
                    zone_redundant = "Enabled"
                elif zone_flag is False:
                    zone_redundant = "Disabled"
                else:
                    zone_redundant = "Not configured"

                # App Service Plan block
                fa_dict["app_service_plan"] = {
                    "id": server_farm_id,
                    "name": plan_name,
                    "resource_group": plan_rg,
                    "location": plan_location,
                    "pricing_plan": sku_name or sku_tier,
                    "instance_count": instance_count,
                    "apps": apps_count,
                    "operating_system": operating_system,
                    "zone_redundant": zone_redundant,
                }

                # Raw networking fields
                networking_raw = {
                    "public_network_access": site_props.get("publicNetworkAccess"),
                    "app_assigned_address": site_props.get("inboundIpAddress"),
                    "private_endpoints": [],
                    "inbound_addresses": [],
                    "virtual_network_subnet_id": site_props.get("virtualNetworkSubnetId"),
                    "hybrid_connections": [],
                    "outbound_dns": None,
                    "outbound_addresses": [],
                    "nat_gateway": None,
                    "network_security_group": None,
                    "user_defined_route": None,
                }

                # Private endpoints
                try:
                    pe_list = functions_conn.list_private_endpoint_connections(resource_group, fa_dict.get("name"))
                    for pe in pe_list or []:
                        pe_props = (pe.get("properties") or {})
                        networking_raw["private_endpoints"].append(
                            {
                                "name": pe.get("name"),
                                "ip_addresses": pe_props.get("ipAddresses"),
                                "private_endpoint_id": (pe_props.get("privateEndpoint") or {}).get("id"),
                                "status": (pe_props.get("privateLinkServiceConnectionState") or {}).get("status"),
                            }
                        )
                except Exception:
                    _LOGGER.warning("[FunctionsManager] private endpoint fetch failed", exc_info=True)

                # Inbound addresses
                inbound_ip = networking_raw.get("app_assigned_address")
                if inbound_ip:
                    networking_raw["inbound_addresses"].append(inbound_ip)

                for pe in networking_raw["private_endpoints"]:
                    for ip in pe.get("ip_addresses") or []:
                        if ip:
                            networking_raw["inbound_addresses"].append(ip)

                # Outbound IPs
                for raw_ips in [site_props.get("outboundIpAddresses"), site_props.get("possibleOutboundIpAddresses")]:
                    if raw_ips:
                        networking_raw["outbound_addresses"].extend(
                            [ip.strip() for ip in raw_ips.split(",") if ip.strip()]
                        )

                # VNet / Subnet metadata
                subnet_id = networking_raw["virtual_network_subnet_id"]
                if subnet_id:
                    try:
                        subnet = functions_conn.get_subnet(subnet_id) or {}
                        subnet_props = (subnet.get("properties") or {})

                        networking_raw["nat_gateway"] = (subnet_props.get("natGateway") or {}).get("id")
                        networking_raw["network_security_group"] = (subnet_props.get("networkSecurityGroup") or {}).get("id")
                        networking_raw["user_defined_route"] = (subnet_props.get("routeTable") or {}).get("id")

                        vnet_id = subnet_id.split("/subnets/")[0]
                        vnet = functions_conn.get_virtual_network(vnet_id) or {}
                        dhcp = (vnet.get("properties") or {}).get("dhcpOptions") or {}
                        dns_servers = dhcp.get("dnsServers")

                        networking_raw["outbound_dns"] = ", ".join(dns_servers) if dns_servers else "Default (Azure-provided)"
                    except Exception:
                        _LOGGER.warning("[FunctionsManager] vnet/subnet fetch failed", exc_info=True)
                        networking_raw["outbound_dns"] = networking_raw["outbound_dns"] or "Default (Azure-provided)"
                else:
                    networking_raw["outbound_dns"] = "Default (Azure-provided)"

                # Hybrid connections
                try:
                    hc_list = functions_conn.list_hybrid_connections(resource_group, fa_dict.get("name"))
                    for hc in hc_list or []:
                        hc_props = (hc.get("properties") or {})
                        networking_raw["hybrid_connections"].append(
                            {
                                "name": hc.get("name"),
                                "hostname": hc_props.get("hostname"),
                                "port": hc_props.get("port"),
                                "service_bus_namespace": hc_props.get("serviceBusNamespace"),
                                "relay_name": hc_props.get("relayName"),
                            }
                        )
                except Exception:
                    _LOGGER.warning("[FunctionsManager] hybrid connections fetch failed", exc_info=True)

                # Networking display formatting
                sku_name_upper = (sku_name or "").upper()
                tier_upper = (pricing_tier or "").upper()
                is_consumption_plan = (sku_name_upper == "Y1" or tier_upper == "DYNAMIC")

                networking = {}

                # Public network access
                pna = networking_raw["public_network_access"]
                if pna is None:
                    networking["public_network_access"] = "Not configured"
                elif str(pna).lower() == "enabled":
                    networking["public_network_access"] = "Enabled (default behavior)"
                elif str(pna).lower() == "disabled":
                    networking["public_network_access"] = "Disabled"
                else:
                    networking["public_network_access"] = str(pna)

                # App assigned address
                networking["app_assigned_address"] = (
                    networking_raw["app_assigned_address"] or "Not configured"
                )

                # Private endpoints
                if networking_raw["private_endpoints"]:
                    names = [pe.get("name") for pe in networking_raw["private_endpoints"] if pe.get("name")]
                    networking["private_endpoints"] = ", ".join(names) if names else f"{len(names)} endpoint(s)"
                else:
                    networking["private_endpoints"] = (
                        "Not supported" if is_consumption_plan else "Not configured"
                    )

                # Inbound addresses
                if networking_raw["inbound_addresses"]:
                    uniq = sorted(set(networking_raw["inbound_addresses"]))
                    networking["inbound_addresses"] = ", ".join(uniq)
                else:
                    networking["inbound_addresses"] = "Dynamic"

                # VNet integration
                if subnet_id:
                    networking["virtual_network_integration"] = subnet_id.split("/subnets/")[-1]
                else:
                    networking["virtual_network_integration"] = (
                        "Not supported" if is_consumption_plan else "Not configured"
                    )

                # Hybrid connections
                if networking_raw["hybrid_connections"]:
                    names = [hc.get("name") for hc in networking_raw["hybrid_connections"] if hc.get("name")]
                    networking["hybrid_connections"] = ", ".join(names) if names else "Configured"
                else:
                    networking["hybrid_connections"] = (
                        "Not supported" if is_consumption_plan else "Not configured"
                    )

                # Outbound DNS
                networking["outbound_dns"] = networking_raw["outbound_dns"] or "Default (Azure-provided)"

                # Outbound addresses
                if networking_raw["outbound_addresses"]:
                    uniq = sorted(set(networking_raw["outbound_addresses"]))
                    networking["outbound_addresses"] = ", ".join(uniq)
                else:
                    networking["outbound_addresses"] = "Dynamic"

                # NAT / NSG / UDR
                if subnet_id:
                    networking["nat_gateway"] = networking_raw["nat_gateway"] or "Not configured"
                    networking["network_security_group"] = networking_raw["network_security_group"] or "Not configured"
                    networking["user_defined_route"] = networking_raw["user_defined_route"] or "Not configured"
                else:
                    networking["nat_gateway"] = "N/A"
                    networking["network_security_group"] = "N/A"
                    networking["user_defined_route"] = "N/A"

                # Save networking data
                fa_dict["networking_raw"] = networking_raw
                fa_dict["networking"] = networking

                # Common metadata
                fa_dict = self.update_tenant_id_from_secret_data(fa_dict, secret_data)
                fa_dict.update(
                    {
                        "resource_group": resource_group,
                        "subscription_id": subscription_info["subscription_id"],
                        "subscription_name": subscription_info["display_name"],
                        "azure_monitor": {"resource_id": resource_id},
                    }
                )

                self.set_region_code(location)

                # Instance type
                sku = plan_sku or {}
                instance_type = sku.get("name") or fa_dict.get("server_farm_id") or "UNKNOWN"

                # Build CloudService
                cloud_services.append(
                    make_cloud_service(
                        name=fa_dict.get("name"),
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=fa_dict,
                        account=secret_data["subscription_id"],
                        instance_type=instance_type,
                        region_code=location,
                        reference=self.make_reference(resource_id),
                        tags=fa_dict.get("tags", {}),
                        data_format="dict",
                    )
                )

            except Exception as e:
                _LOGGER.error("[FunctionsManager.create_cloud_service] Error: %s", e, exc_info=True)
                error_responses.append(
                    make_error_response(
                        error=e,
                        provider=self.provider,
                        cloud_service_group=self.cloud_service_group,
                        cloud_service_type=self.cloud_service_type,
                    )
                )

        return cloud_services, error_responses
