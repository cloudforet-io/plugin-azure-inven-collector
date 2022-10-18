from schematics import Model
from schematics.types import ModelType, DictType, StringType, ListType, IntType, BooleanType, DateTimeType, FloatType
from spaceone.inventory.libs.schema.resource import AzureCloudService


# ContainerGroupIdentity
class UserAssignedIdentity(Model):
    client_id = StringType(serialize_when_none=False)
    principal_id = StringType(serialize_when_none=False)


class ContainerGroupIdentity(Model):
    principal_id = StringType(serialize_when_none=False)
    tenant_id = StringType(serialize_when_none=False)
    type = StringType(choices=('NONE', 'SYSTEM_ASSIGNED', 'SYSTEM_ASSIGNED_USER_ASSIGNED', 'USER_ASSIGNED'), serialize_when_none=False)
    user_assigned_identities = DictType(StringType(), ModelType(UserAssignedIdentity), serialize_when_none=False)


# Container
class ContainerPort(Model):
    protocol = StringType(choices=('TCP', 'UDP'), default='TCP')
    port = StringType(serialize_when_none=False)


class EnvironmentVariable(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)
    secure_value = StringType(serialize_when_none=False)


# Container - ContainerPropertiesInstanceView
class ContainerState(Model):
    state = StringType(serialize_when_none=False)
    start_time = DateTimeType(serialize_when_none=False)
    exit_code = IntType(serialize_when_none=False)
    finish_time = DateTimeType(serialize_when_none=False)
    detail_status = StringType(serialize_when_none=False)


class Event(Model):
    count = IntType(serialize_when_none=False)
    first_timestamp = DateTimeType(serialize_when_none=False)
    last_timestamp = DateTimeType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class ContainerPropertiesInstanceView(Model):
    restart_count = IntType(serialize_when_none=False)
    current_state = ModelType(ContainerState, serialize_when_none=False)
    previous_state = ModelType(ContainerState, serialize_when_none=False)
    events = ListType(ModelType(Event), serialize_when_none=False)


# Container - ResourceRequirements
class GpuResource(Model):
    count = IntType(serialize_when_none=False)
    sku = StringType(choices=('K80', 'P100', 'V100'), serialize_when_none=False)


class ResourceRequests(Model):
    memory_in_gb = FloatType(serialize_when_none=False)
    cpu = FloatType(serialize_when_none=False)
    gpu = ModelType(GpuResource, serialize_when_none=False)


class ResourceLimits(Model):
    memory_in_gb = FloatType(serialize_when_none=False)
    cpu = FloatType(serialize_when_none=False)
    gpu = ModelType(GpuResource, serialize_when_none=False)


class ResourceRequirements(Model):
    requests = ModelType(ResourceRequests, serialize_when_none=False)
    limits = ModelType(ResourceLimits, serialize_when_none=False)


# Container - VolumeMount
class VolumeMount(Model):
    name = StringType(serialize_when_none=False)
    mount_path = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


# Container - ContainerProbe
class ContainerExec(Model):
    command = ListType(StringType(serialize_when_none=False))


class HttpHeader(Model):
    name = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class ContainerHttpGet(Model):
    path = StringType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    scheme = StringType(choices=('HTTP', 'HTTPS'), serialize_when_none=False)
    http_headers = ListType(ModelType(HttpHeader), serialize_when_none=False)


class ContainerProbe(Model):
    exec_property = ModelType(ContainerExec, serialize_when_none=False)
    http_get = ModelType(ContainerHttpGet, serialize_when_none=False)
    initial_delay_seconds = IntType(serialize_when_none=False)
    period_seconds = IntType(serialize_when_none=False)
    failure_threshold = IntType(serialize_when_none=False)
    success_threshold = IntType(serialize_when_none=False)
    timeout_seconds = IntType(serialize_when_none=False)


class Container(Model):
    name = StringType(serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    command = ListType(StringType, serialize_when_none=False)
    ports = ListType(ModelType(ContainerPort), serialize_when_none=False)
    environment_variables = ListType(ModelType(EnvironmentVariable), serialize_when_none=False)
    instance_view = ModelType(ContainerPropertiesInstanceView)
    resources = ModelType(ResourceRequirements, serialize_when_none=False)
    volume_mounts = ListType(ModelType(VolumeMount), serialize_when_none=None)
    liveness_probe = ModelType(ContainerProbe, serialize_when_none=False)
    readiness_probe = ModelType(ContainerProbe, serialize_when_none=False)


# ImageRegistryCredential
class ImageRegistryCredential(Model):
    server = StringType(serialize_when_none=False)
    username = StringType(serialize_when_none=False)
    password = StringType(serialize_when_none=False)
    identity = StringType(serialize_when_none=False)
    identity_url = StringType(serialize_when_none=False)


# IpAddress
class Port(ContainerPort):
    pass


class IpAddress(Model):
    ports = ListType(ModelType(Port), serialize_when_none=False)
    type = StringType(choices=('PRIVATE', 'PUBLIC'))
    ip = StringType(serialize_when_none=False)
    dns_name_label = StringType(serialize_when_none=False)
    auto_generated_domain_name_label_scope = StringType(choices=('NOREUSE', 'RESOURCE_GROUP_REUSE', 'SUBSCRIPTION_REUSE',
                                                                 'TENANT_REUSE', 'UNSECURE'))
    fqdn = StringType(serialize_when_none=False)


# Volume

# Volume - AzureFileVolume
class AzureFileVolume(Model):
    share_name = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    storage_account_name = StringType(serialize_when_none=False)
    storage_account_key = StringType(serialize_when_none=False)


# Volume - GitRepoVolume
class GitRepoVolume(Model):
    directory = StringType(serialize_when_none=False)
    repository = StringType(serialize_when_none=False)
    revision = StringType(serialize_when_none=False)


class Volume(Model):
    name = StringType(serialize_when_none=False)
    azure_file = ModelType(AzureFileVolume, serialize_when_none=False)
    empty_dir = DictType(StringType(), StringType())
    secret = DictType(StringType(), StringType(), serialize_when_none=False)
    git_repo = ModelType(GitRepoVolume, serialize_when_none=False)


# ContainerGroupPropertiesInstanceView
class ContainerGroupPropertiesInstanceView(Model):
    events = ListType(ModelType(Event))
    state = StringType(serialize_when_none=False)

# ContainerGroupDiagnostics


# ContainerGroupDiagnostics LogAnalytics
class LogAnalytics(Model):
    workspace_id = StringType(serialize_when_none=False)
    workspace_key = StringType(serialize_when_none=False)
    log_type = StringType(choices=('CONTAINER_INSIGHTS', 'CONTAINER_INSTANCE_LOGS'))
    metadata = DictType(StringType(), StringType(), serialize_when_none=False)
    workspace_resource_id = StringType(serialize_when_none=False)


class ContainerGroupDiagnostics(Model):
    log_analytics = ModelType(LogAnalytics, serialize_when_none=False)


# ContainerGroupSubnetId
class ContainerGroupSubnetId(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


# DnsConfiguration
class DnsConfiguration(Model):
    name_servers = ListType(StringType, serialize_when_none=False)
    search_domains = StringType(serialize_when_none=False)
    options = StringType(serialize_when_none=False)


# EncryptionProperties
class EncryptionProperties(Model):
    vault_base_url = StringType(serialize_when_none=False)
    key_name = StringType(serialize_when_none=False)
    key_version = StringType(serialize_when_none=False)

# InitContainerDefinition


# InitContainerDefinition - InitContainerPropertiesDefinitionInstanceView
class InitContainerPropertiesDefinitionInstanceView(ContainerPropertiesInstanceView):
    pass


class InitContainerDefinition(Model):
    name = StringType(serialize_when_none=False)
    image = StringType(serialize_when_none=False)
    command = ListType(StringType, serialize_when_none=False)
    environment_variables = ListType(ModelType(EnvironmentVariable), serialize_when_none=False)
    instance_view = ModelType(InitContainerPropertiesDefinitionInstanceView, serialize_when_none=False)
    volume_mounts = ListType(ModelType(VolumeMount), serialize_when_none=False)


class ContainerInstance(AzureCloudService):  # Main Class
    id = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    identity = ModelType(ContainerGroupIdentity)
    provisioning_state = StringType(serialize_when_none=False)
    containers = ListType(ModelType(Container), serialize_when_none=False)
    image_registry_credentials = ListType(ModelType(ImageRegistryCredential), serialize_when_none=False)
    restart_policy = StringType(choices=('ALWAYS', 'NEVER', 'ON_FAILURE'), serialize_when_none=False)
    ip_address = ModelType(IpAddress, serialize_when_none=False)
    os_type = StringType(choices=('LINUX', 'WINDOWS'))
    volumes = ListType(ModelType(Volume), serialize_when_none=False)
    instance_view = ModelType(ContainerGroupPropertiesInstanceView, serialize_when_none=False)
    diagnostics = ModelType(ContainerGroupDiagnostics, serialize_when_none=False)
    subnet_ids = ListType(ModelType(ContainerGroupSubnetId), serialize_when_none=False)
    dns_config = ModelType(DnsConfiguration, serialize_when_none=False)
    sku = StringType(choices=('DEDICATED', 'STANDARD'), serialize_when_none=False)
    encryption_properties = ModelType(EncryptionProperties, serialize_when_none=False)
    init_containers = ListType(ModelType(InitContainerDefinition), serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    zones = ListType(StringType, serialize_when_none=False)
    container_count_display = IntType(serialize_when_none=False)
    start_time = DateTimeType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }