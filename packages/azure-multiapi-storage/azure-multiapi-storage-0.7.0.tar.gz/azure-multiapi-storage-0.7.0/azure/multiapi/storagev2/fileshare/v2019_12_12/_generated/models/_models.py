# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model
from azure.core.exceptions import HttpResponseError


class AccessPolicy(Model):
    """An Access policy.

    :param start: The date-time the policy is active.
    :type start: str
    :param expiry: The date-time the policy expires.
    :type expiry: str
    :param permission: The permissions for the ACL policy.
    :type permission: str
    """

    _attribute_map = {
        'start': {'key': 'Start', 'type': 'str', 'xml': {'name': 'Start'}},
        'expiry': {'key': 'Expiry', 'type': 'str', 'xml': {'name': 'Expiry'}},
        'permission': {'key': 'Permission', 'type': 'str', 'xml': {'name': 'Permission'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(AccessPolicy, self).__init__(**kwargs)
        self.start = kwargs.get('start', None)
        self.expiry = kwargs.get('expiry', None)
        self.permission = kwargs.get('permission', None)


class CopyFileSmbInfo(Model):
    """Additional parameters for start_copy operation.

    :param file_permission_copy_mode: Specifies the option to copy file
     security descriptor from source file or to set it using the value which is
     defined by the header value of x-ms-file-permission or
     x-ms-file-permission-key. Possible values include: 'source', 'override'
    :type file_permission_copy_mode: str or
     ~azure.storage.fileshare.models.PermissionCopyModeType
    :param ignore_read_only: Specifies the option to overwrite the target file
     if it already exists and has read-only attribute set.
    :type ignore_read_only: bool
    :param file_attributes: Specifies either the option to copy file
     attributes from a source file(source) to a target file or a list of
     attributes to set on a target file.
    :type file_attributes: str
    :param file_creation_time: Specifies either the option to copy file
     creation time from a source file(source) to a target file or a time value
     in ISO 8601 format to set as creation time on a target file.
    :type file_creation_time: str
    :param file_last_write_time: Specifies either the option to copy file last
     write time from a source file(source) to a target file or a time value in
     ISO 8601 format to set as last write time on a target file.
    :type file_last_write_time: str
    :param set_archive_attribute: Specifies the option to set archive
     attribute on a target file. True means archive attribute will be set on a
     target file despite attribute overrides or a source file state.
    :type set_archive_attribute: bool
    """

    _attribute_map = {
        'file_permission_copy_mode': {'key': '', 'type': 'PermissionCopyModeType', 'xml': {'name': 'file_permission_copy_mode'}},
        'ignore_read_only': {'key': '', 'type': 'bool', 'xml': {'name': 'ignore_read_only'}},
        'file_attributes': {'key': '', 'type': 'str', 'xml': {'name': 'file_attributes'}},
        'file_creation_time': {'key': '', 'type': 'str', 'xml': {'name': 'file_creation_time'}},
        'file_last_write_time': {'key': '', 'type': 'str', 'xml': {'name': 'file_last_write_time'}},
        'set_archive_attribute': {'key': '', 'type': 'bool', 'xml': {'name': 'set_archive_attribute'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(CopyFileSmbInfo, self).__init__(**kwargs)
        self.file_permission_copy_mode = kwargs.get('file_permission_copy_mode', None)
        self.ignore_read_only = kwargs.get('ignore_read_only', None)
        self.file_attributes = kwargs.get('file_attributes', None)
        self.file_creation_time = kwargs.get('file_creation_time', None)
        self.file_last_write_time = kwargs.get('file_last_write_time', None)
        self.set_archive_attribute = kwargs.get('set_archive_attribute', None)


class CorsRule(Model):
    """CORS is an HTTP feature that enables a web application running under one
    domain to access resources in another domain. Web browsers implement a
    security restriction known as same-origin policy that prevents a web page
    from calling APIs in a different domain; CORS provides a secure way to
    allow one domain (the origin domain) to call APIs in another domain.

    All required parameters must be populated in order to send to Azure.

    :param allowed_origins: Required. The origin domains that are permitted to
     make a request against the storage service via CORS. The origin domain is
     the domain from which the request originates. Note that the origin must be
     an exact case-sensitive match with the origin that the user age sends to
     the service. You can also use the wildcard character '*' to allow all
     origin domains to make requests via CORS.
    :type allowed_origins: str
    :param allowed_methods: Required. The methods (HTTP request verbs) that
     the origin domain may use for a CORS request. (comma separated)
    :type allowed_methods: str
    :param allowed_headers: Required. The request headers that the origin
     domain may specify on the CORS request.
    :type allowed_headers: str
    :param exposed_headers: Required. The response headers that may be sent in
     the response to the CORS request and exposed by the browser to the request
     issuer.
    :type exposed_headers: str
    :param max_age_in_seconds: Required. The maximum amount time that a
     browser should cache the preflight OPTIONS request.
    :type max_age_in_seconds: int
    """

    _validation = {
        'allowed_origins': {'required': True},
        'allowed_methods': {'required': True},
        'allowed_headers': {'required': True},
        'exposed_headers': {'required': True},
        'max_age_in_seconds': {'required': True, 'minimum': 0},
    }

    _attribute_map = {
        'allowed_origins': {'key': 'AllowedOrigins', 'type': 'str', 'xml': {'name': 'AllowedOrigins'}},
        'allowed_methods': {'key': 'AllowedMethods', 'type': 'str', 'xml': {'name': 'AllowedMethods'}},
        'allowed_headers': {'key': 'AllowedHeaders', 'type': 'str', 'xml': {'name': 'AllowedHeaders'}},
        'exposed_headers': {'key': 'ExposedHeaders', 'type': 'str', 'xml': {'name': 'ExposedHeaders'}},
        'max_age_in_seconds': {'key': 'MaxAgeInSeconds', 'type': 'int', 'xml': {'name': 'MaxAgeInSeconds'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(CorsRule, self).__init__(**kwargs)
        self.allowed_origins = kwargs.get('allowed_origins', None)
        self.allowed_methods = kwargs.get('allowed_methods', None)
        self.allowed_headers = kwargs.get('allowed_headers', None)
        self.exposed_headers = kwargs.get('exposed_headers', None)
        self.max_age_in_seconds = kwargs.get('max_age_in_seconds', None)


class DirectoryItem(Model):
    """A listed directory item.

    All required parameters must be populated in order to send to Azure.

    :param name: Required.
    :type name: str
    """

    _validation = {
        'name': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str', 'xml': {'name': 'Name'}},
    }
    _xml_map = {
        'name': 'Directory'
    }

    def __init__(self, **kwargs):
        super(DirectoryItem, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)


class FileHTTPHeaders(Model):
    """Additional parameters for a set of operations, such as: File_create,
    File_set_http_headers.

    :param file_content_type: Sets the MIME content type of the file. The
     default type is 'application/octet-stream'.
    :type file_content_type: str
    :param file_content_encoding: Specifies which content encodings have been
     applied to the file.
    :type file_content_encoding: str
    :param file_content_language: Specifies the natural languages used by this
     resource.
    :type file_content_language: str
    :param file_cache_control: Sets the file's cache control. The File service
     stores this value but does not use or modify it.
    :type file_cache_control: str
    :param file_content_md5: Sets the file's MD5 hash.
    :type file_content_md5: bytearray
    :param file_content_disposition: Sets the file's Content-Disposition
     header.
    :type file_content_disposition: str
    """

    _attribute_map = {
        'file_content_type': {'key': '', 'type': 'str', 'xml': {'name': 'file_content_type'}},
        'file_content_encoding': {'key': '', 'type': 'str', 'xml': {'name': 'file_content_encoding'}},
        'file_content_language': {'key': '', 'type': 'str', 'xml': {'name': 'file_content_language'}},
        'file_cache_control': {'key': '', 'type': 'str', 'xml': {'name': 'file_cache_control'}},
        'file_content_md5': {'key': '', 'type': 'bytearray', 'xml': {'name': 'file_content_md5'}},
        'file_content_disposition': {'key': '', 'type': 'str', 'xml': {'name': 'file_content_disposition'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(FileHTTPHeaders, self).__init__(**kwargs)
        self.file_content_type = kwargs.get('file_content_type', None)
        self.file_content_encoding = kwargs.get('file_content_encoding', None)
        self.file_content_language = kwargs.get('file_content_language', None)
        self.file_cache_control = kwargs.get('file_cache_control', None)
        self.file_content_md5 = kwargs.get('file_content_md5', None)
        self.file_content_disposition = kwargs.get('file_content_disposition', None)


class FileItem(Model):
    """A listed file item.

    All required parameters must be populated in order to send to Azure.

    :param name: Required.
    :type name: str
    :param properties: Required.
    :type properties: ~azure.storage.fileshare.models.FileProperty
    """

    _validation = {
        'name': {'required': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str', 'xml': {'name': 'Name'}},
        'properties': {'key': 'Properties', 'type': 'FileProperty', 'xml': {'name': 'Properties'}},
    }
    _xml_map = {
        'name': 'File'
    }

    def __init__(self, **kwargs):
        super(FileItem, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.properties = kwargs.get('properties', None)


class FileProperty(Model):
    """File properties.

    All required parameters must be populated in order to send to Azure.

    :param content_length: Required. Content length of the file. This value
     may not be up-to-date since an SMB client may have modified the file
     locally. The value of Content-Length may not reflect that fact until the
     handle is closed or the op-lock is broken. To retrieve current property
     values, call Get File Properties.
    :type content_length: long
    """

    _validation = {
        'content_length': {'required': True},
    }

    _attribute_map = {
        'content_length': {'key': 'Content-Length', 'type': 'long', 'xml': {'name': 'Content-Length'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(FileProperty, self).__init__(**kwargs)
        self.content_length = kwargs.get('content_length', None)


class FilesAndDirectoriesListSegment(Model):
    """Abstract for entries that can be listed from Directory.

    All required parameters must be populated in order to send to Azure.

    :param directory_items: Required.
    :type directory_items: list[~azure.storage.fileshare.models.DirectoryItem]
    :param file_items: Required.
    :type file_items: list[~azure.storage.fileshare.models.FileItem]
    """

    _validation = {
        'directory_items': {'required': True},
        'file_items': {'required': True},
    }

    _attribute_map = {
        'directory_items': {'key': 'DirectoryItems', 'type': '[DirectoryItem]', 'xml': {'name': 'DirectoryItems', 'itemsName': 'Directory'}},
        'file_items': {'key': 'FileItems', 'type': '[FileItem]', 'xml': {'name': 'FileItems', 'itemsName': 'File'}},
    }
    _xml_map = {
        'name': 'Entries'
    }

    def __init__(self, **kwargs):
        super(FilesAndDirectoriesListSegment, self).__init__(**kwargs)
        self.directory_items = kwargs.get('directory_items', None)
        self.file_items = kwargs.get('file_items', None)


class HandleItem(Model):
    """A listed Azure Storage handle item.

    All required parameters must be populated in order to send to Azure.

    :param handle_id: Required. XSMB service handle ID
    :type handle_id: str
    :param path: Required. File or directory name including full path starting
     from share root
    :type path: str
    :param file_id: Required. FileId uniquely identifies the file or
     directory.
    :type file_id: str
    :param parent_id: ParentId uniquely identifies the parent directory of the
     object.
    :type parent_id: str
    :param session_id: Required. SMB session ID in context of which the file
     handle was opened
    :type session_id: str
    :param client_ip: Required. Client IP that opened the handle
    :type client_ip: str
    :param open_time: Required. Time when the session that previously opened
     the handle has last been reconnected. (UTC)
    :type open_time: datetime
    :param last_reconnect_time: Time handle was last connected to (UTC)
    :type last_reconnect_time: datetime
    """

    _validation = {
        'handle_id': {'required': True},
        'path': {'required': True},
        'file_id': {'required': True},
        'session_id': {'required': True},
        'client_ip': {'required': True},
        'open_time': {'required': True},
    }

    _attribute_map = {
        'handle_id': {'key': 'HandleId', 'type': 'str', 'xml': {'name': 'HandleId'}},
        'path': {'key': 'Path', 'type': 'str', 'xml': {'name': 'Path'}},
        'file_id': {'key': 'FileId', 'type': 'str', 'xml': {'name': 'FileId'}},
        'parent_id': {'key': 'ParentId', 'type': 'str', 'xml': {'name': 'ParentId'}},
        'session_id': {'key': 'SessionId', 'type': 'str', 'xml': {'name': 'SessionId'}},
        'client_ip': {'key': 'ClientIp', 'type': 'str', 'xml': {'name': 'ClientIp'}},
        'open_time': {'key': 'OpenTime', 'type': 'rfc-1123', 'xml': {'name': 'OpenTime'}},
        'last_reconnect_time': {'key': 'LastReconnectTime', 'type': 'rfc-1123', 'xml': {'name': 'LastReconnectTime'}},
    }
    _xml_map = {
        'name': 'Handle'
    }

    def __init__(self, **kwargs):
        super(HandleItem, self).__init__(**kwargs)
        self.handle_id = kwargs.get('handle_id', None)
        self.path = kwargs.get('path', None)
        self.file_id = kwargs.get('file_id', None)
        self.parent_id = kwargs.get('parent_id', None)
        self.session_id = kwargs.get('session_id', None)
        self.client_ip = kwargs.get('client_ip', None)
        self.open_time = kwargs.get('open_time', None)
        self.last_reconnect_time = kwargs.get('last_reconnect_time', None)


class LeaseAccessConditions(Model):
    """Additional parameters for a set of operations.

    :param lease_id: If specified, the operation only succeeds if the
     resource's lease is active and matches this ID.
    :type lease_id: str
    """

    _attribute_map = {
        'lease_id': {'key': '', 'type': 'str', 'xml': {'name': 'lease_id'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(LeaseAccessConditions, self).__init__(**kwargs)
        self.lease_id = kwargs.get('lease_id', None)


class ListFilesAndDirectoriesSegmentResponse(Model):
    """An enumeration of directories and files.

    All required parameters must be populated in order to send to Azure.

    :param service_endpoint: Required.
    :type service_endpoint: str
    :param share_name: Required.
    :type share_name: str
    :param share_snapshot:
    :type share_snapshot: str
    :param directory_path: Required.
    :type directory_path: str
    :param prefix: Required.
    :type prefix: str
    :param marker:
    :type marker: str
    :param max_results:
    :type max_results: int
    :param segment: Required.
    :type segment:
     ~azure.storage.fileshare.models.FilesAndDirectoriesListSegment
    :param next_marker: Required.
    :type next_marker: str
    """

    _validation = {
        'service_endpoint': {'required': True},
        'share_name': {'required': True},
        'directory_path': {'required': True},
        'prefix': {'required': True},
        'segment': {'required': True},
        'next_marker': {'required': True},
    }

    _attribute_map = {
        'service_endpoint': {'key': 'ServiceEndpoint', 'type': 'str', 'xml': {'name': 'ServiceEndpoint', 'attr': True}},
        'share_name': {'key': 'ShareName', 'type': 'str', 'xml': {'name': 'ShareName', 'attr': True}},
        'share_snapshot': {'key': 'ShareSnapshot', 'type': 'str', 'xml': {'name': 'ShareSnapshot', 'attr': True}},
        'directory_path': {'key': 'DirectoryPath', 'type': 'str', 'xml': {'name': 'DirectoryPath', 'attr': True}},
        'prefix': {'key': 'Prefix', 'type': 'str', 'xml': {'name': 'Prefix'}},
        'marker': {'key': 'Marker', 'type': 'str', 'xml': {'name': 'Marker'}},
        'max_results': {'key': 'MaxResults', 'type': 'int', 'xml': {'name': 'MaxResults'}},
        'segment': {'key': 'Segment', 'type': 'FilesAndDirectoriesListSegment', 'xml': {'name': 'Segment'}},
        'next_marker': {'key': 'NextMarker', 'type': 'str', 'xml': {'name': 'NextMarker'}},
    }
    _xml_map = {
        'name': 'EnumerationResults'
    }

    def __init__(self, **kwargs):
        super(ListFilesAndDirectoriesSegmentResponse, self).__init__(**kwargs)
        self.service_endpoint = kwargs.get('service_endpoint', None)
        self.share_name = kwargs.get('share_name', None)
        self.share_snapshot = kwargs.get('share_snapshot', None)
        self.directory_path = kwargs.get('directory_path', None)
        self.prefix = kwargs.get('prefix', None)
        self.marker = kwargs.get('marker', None)
        self.max_results = kwargs.get('max_results', None)
        self.segment = kwargs.get('segment', None)
        self.next_marker = kwargs.get('next_marker', None)


class ListHandlesResponse(Model):
    """An enumeration of handles.

    All required parameters must be populated in order to send to Azure.

    :param handle_list:
    :type handle_list: list[~azure.storage.fileshare.models.HandleItem]
    :param next_marker: Required.
    :type next_marker: str
    """

    _validation = {
        'next_marker': {'required': True},
    }

    _attribute_map = {
        'handle_list': {'key': 'HandleList', 'type': '[HandleItem]', 'xml': {'name': 'Entries', 'itemsName': 'Entries', 'wrapped': True}},
        'next_marker': {'key': 'NextMarker', 'type': 'str', 'xml': {'name': 'NextMarker'}},
    }
    _xml_map = {
        'name': 'EnumerationResults'
    }

    def __init__(self, **kwargs):
        super(ListHandlesResponse, self).__init__(**kwargs)
        self.handle_list = kwargs.get('handle_list', None)
        self.next_marker = kwargs.get('next_marker', None)


class ListSharesResponse(Model):
    """An enumeration of shares.

    All required parameters must be populated in order to send to Azure.

    :param service_endpoint: Required.
    :type service_endpoint: str
    :param prefix:
    :type prefix: str
    :param marker:
    :type marker: str
    :param max_results:
    :type max_results: int
    :param share_items:
    :type share_items: list[~azure.storage.fileshare.models.ShareItem]
    :param next_marker: Required.
    :type next_marker: str
    """

    _validation = {
        'service_endpoint': {'required': True},
        'next_marker': {'required': True},
    }

    _attribute_map = {
        'service_endpoint': {'key': 'ServiceEndpoint', 'type': 'str', 'xml': {'name': 'ServiceEndpoint', 'attr': True}},
        'prefix': {'key': 'Prefix', 'type': 'str', 'xml': {'name': 'Prefix'}},
        'marker': {'key': 'Marker', 'type': 'str', 'xml': {'name': 'Marker'}},
        'max_results': {'key': 'MaxResults', 'type': 'int', 'xml': {'name': 'MaxResults'}},
        'share_items': {'key': 'ShareItems', 'type': '[ShareItem]', 'xml': {'name': 'Shares', 'itemsName': 'Shares', 'wrapped': True}},
        'next_marker': {'key': 'NextMarker', 'type': 'str', 'xml': {'name': 'NextMarker'}},
    }
    _xml_map = {
        'name': 'EnumerationResults'
    }

    def __init__(self, **kwargs):
        super(ListSharesResponse, self).__init__(**kwargs)
        self.service_endpoint = kwargs.get('service_endpoint', None)
        self.prefix = kwargs.get('prefix', None)
        self.marker = kwargs.get('marker', None)
        self.max_results = kwargs.get('max_results', None)
        self.share_items = kwargs.get('share_items', None)
        self.next_marker = kwargs.get('next_marker', None)


class Metrics(Model):
    """Storage Analytics metrics for file service.

    All required parameters must be populated in order to send to Azure.

    :param version: Required. The version of Storage Analytics to configure.
    :type version: str
    :param enabled: Required. Indicates whether metrics are enabled for the
     File service.
    :type enabled: bool
    :param include_apis: Indicates whether metrics should generate summary
     statistics for called API operations.
    :type include_apis: bool
    :param retention_policy:
    :type retention_policy: ~azure.storage.fileshare.models.RetentionPolicy
    """

    _validation = {
        'version': {'required': True},
        'enabled': {'required': True},
    }

    _attribute_map = {
        'version': {'key': 'Version', 'type': 'str', 'xml': {'name': 'Version'}},
        'enabled': {'key': 'Enabled', 'type': 'bool', 'xml': {'name': 'Enabled'}},
        'include_apis': {'key': 'IncludeAPIs', 'type': 'bool', 'xml': {'name': 'IncludeAPIs'}},
        'retention_policy': {'key': 'RetentionPolicy', 'type': 'RetentionPolicy', 'xml': {'name': 'RetentionPolicy'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(Metrics, self).__init__(**kwargs)
        self.version = kwargs.get('version', None)
        self.enabled = kwargs.get('enabled', None)
        self.include_apis = kwargs.get('include_apis', None)
        self.retention_policy = kwargs.get('retention_policy', None)


class Range(Model):
    """An Azure Storage file range.

    All required parameters must be populated in order to send to Azure.

    :param start: Required. Start of the range.
    :type start: long
    :param end: Required. End of the range.
    :type end: long
    """

    _validation = {
        'start': {'required': True},
        'end': {'required': True},
    }

    _attribute_map = {
        'start': {'key': 'Start', 'type': 'long', 'xml': {'name': 'Start'}},
        'end': {'key': 'End', 'type': 'long', 'xml': {'name': 'End'}},
    }
    _xml_map = {
        'name': 'Range'
    }

    def __init__(self, **kwargs):
        super(Range, self).__init__(**kwargs)
        self.start = kwargs.get('start', None)
        self.end = kwargs.get('end', None)


class RetentionPolicy(Model):
    """The retention policy.

    All required parameters must be populated in order to send to Azure.

    :param enabled: Required. Indicates whether a retention policy is enabled
     for the File service. If false, metrics data is retained, and the user is
     responsible for deleting it.
    :type enabled: bool
    :param days: Indicates the number of days that metrics data should be
     retained. All data older than this value will be deleted. Metrics data is
     deleted on a best-effort basis after the retention period expires.
    :type days: int
    """

    _validation = {
        'enabled': {'required': True},
        'days': {'maximum': 365, 'minimum': 1},
    }

    _attribute_map = {
        'enabled': {'key': 'Enabled', 'type': 'bool', 'xml': {'name': 'Enabled'}},
        'days': {'key': 'Days', 'type': 'int', 'xml': {'name': 'Days'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(RetentionPolicy, self).__init__(**kwargs)
        self.enabled = kwargs.get('enabled', None)
        self.days = kwargs.get('days', None)


class ShareItem(Model):
    """A listed Azure Storage share item.

    All required parameters must be populated in order to send to Azure.

    :param name: Required.
    :type name: str
    :param snapshot:
    :type snapshot: str
    :param deleted:
    :type deleted: bool
    :param version:
    :type version: str
    :param properties: Required.
    :type properties: ~azure.storage.fileshare.models.ShareProperties
    :param metadata:
    :type metadata: dict[str, str]
    """

    _validation = {
        'name': {'required': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str', 'xml': {'name': 'Name'}},
        'snapshot': {'key': 'Snapshot', 'type': 'str', 'xml': {'name': 'Snapshot'}},
        'deleted': {'key': 'Deleted', 'type': 'bool', 'xml': {'name': 'Deleted'}},
        'version': {'key': 'Version', 'type': 'str', 'xml': {'name': 'Version'}},
        'properties': {'key': 'Properties', 'type': 'ShareProperties', 'xml': {'name': 'Properties'}},
        'metadata': {'key': 'Metadata', 'type': '{str}', 'xml': {'name': 'Metadata'}},
    }
    _xml_map = {
        'name': 'Share'
    }

    def __init__(self, **kwargs):
        super(ShareItem, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.snapshot = kwargs.get('snapshot', None)
        self.deleted = kwargs.get('deleted', None)
        self.version = kwargs.get('version', None)
        self.properties = kwargs.get('properties', None)
        self.metadata = kwargs.get('metadata', None)


class SharePermission(Model):
    """A permission (a security descriptor) at the share level.

    All required parameters must be populated in order to send to Azure.

    :param permission: Required. The permission in the Security Descriptor
     Definition Language (SDDL).
    :type permission: str
    """

    _validation = {
        'permission': {'required': True},
    }

    _attribute_map = {
        'permission': {'key': 'permission', 'type': 'str', 'xml': {'name': 'permission'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(SharePermission, self).__init__(**kwargs)
        self.permission = kwargs.get('permission', None)


class ShareProperties(Model):
    """Properties of a share.

    All required parameters must be populated in order to send to Azure.

    :param last_modified: Required.
    :type last_modified: datetime
    :param etag: Required.
    :type etag: str
    :param quota: Required.
    :type quota: int
    :param provisioned_iops:
    :type provisioned_iops: int
    :param provisioned_ingress_mbps:
    :type provisioned_ingress_mbps: int
    :param provisioned_egress_mbps:
    :type provisioned_egress_mbps: int
    :param next_allowed_quota_downgrade_time:
    :type next_allowed_quota_downgrade_time: datetime
    :param deleted_time:
    :type deleted_time: datetime
    :param remaining_retention_days:
    :type remaining_retention_days: int
    """

    _validation = {
        'last_modified': {'required': True},
        'etag': {'required': True},
        'quota': {'required': True},
    }

    _attribute_map = {
        'last_modified': {'key': 'Last-Modified', 'type': 'rfc-1123', 'xml': {'name': 'Last-Modified'}},
        'etag': {'key': 'Etag', 'type': 'str', 'xml': {'name': 'Etag'}},
        'quota': {'key': 'Quota', 'type': 'int', 'xml': {'name': 'Quota'}},
        'provisioned_iops': {'key': 'ProvisionedIops', 'type': 'int', 'xml': {'name': 'ProvisionedIops'}},
        'provisioned_ingress_mbps': {'key': 'ProvisionedIngressMBps', 'type': 'int', 'xml': {'name': 'ProvisionedIngressMBps'}},
        'provisioned_egress_mbps': {'key': 'ProvisionedEgressMBps', 'type': 'int', 'xml': {'name': 'ProvisionedEgressMBps'}},
        'next_allowed_quota_downgrade_time': {'key': 'NextAllowedQuotaDowngradeTime', 'type': 'rfc-1123', 'xml': {'name': 'NextAllowedQuotaDowngradeTime'}},
        'deleted_time': {'key': 'DeletedTime', 'type': 'rfc-1123', 'xml': {'name': 'DeletedTime'}},
        'remaining_retention_days': {'key': 'RemainingRetentionDays', 'type': 'int', 'xml': {'name': 'RemainingRetentionDays'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(ShareProperties, self).__init__(**kwargs)
        self.last_modified = kwargs.get('last_modified', None)
        self.etag = kwargs.get('etag', None)
        self.quota = kwargs.get('quota', None)
        self.provisioned_iops = kwargs.get('provisioned_iops', None)
        self.provisioned_ingress_mbps = kwargs.get('provisioned_ingress_mbps', None)
        self.provisioned_egress_mbps = kwargs.get('provisioned_egress_mbps', None)
        self.next_allowed_quota_downgrade_time = kwargs.get('next_allowed_quota_downgrade_time', None)
        self.deleted_time = kwargs.get('deleted_time', None)
        self.remaining_retention_days = kwargs.get('remaining_retention_days', None)


class ShareStats(Model):
    """Stats for the share.

    All required parameters must be populated in order to send to Azure.

    :param share_usage_bytes: Required. The approximate size of the data
     stored in bytes. Note that this value may not include all recently created
     or recently resized files.
    :type share_usage_bytes: int
    """

    _validation = {
        'share_usage_bytes': {'required': True},
    }

    _attribute_map = {
        'share_usage_bytes': {'key': 'ShareUsageBytes', 'type': 'int', 'xml': {'name': 'ShareUsageBytes'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(ShareStats, self).__init__(**kwargs)
        self.share_usage_bytes = kwargs.get('share_usage_bytes', None)


class SignedIdentifier(Model):
    """Signed identifier.

    All required parameters must be populated in order to send to Azure.

    :param id: Required. A unique id.
    :type id: str
    :param access_policy: The access policy.
    :type access_policy: ~azure.storage.fileshare.models.AccessPolicy
    """

    _validation = {
        'id': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'str', 'xml': {'name': 'Id'}},
        'access_policy': {'key': 'AccessPolicy', 'type': 'AccessPolicy', 'xml': {'name': 'AccessPolicy'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(SignedIdentifier, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.access_policy = kwargs.get('access_policy', None)


class SourceModifiedAccessConditions(Model):
    """Additional parameters for upload_range_from_url operation.

    :param source_if_match_crc64: Specify the crc64 value to operate only on
     range with a matching crc64 checksum.
    :type source_if_match_crc64: bytearray
    :param source_if_none_match_crc64: Specify the crc64 value to operate only
     on range without a matching crc64 checksum.
    :type source_if_none_match_crc64: bytearray
    """

    _attribute_map = {
        'source_if_match_crc64': {'key': '', 'type': 'bytearray', 'xml': {'name': 'source_if_match_crc64'}},
        'source_if_none_match_crc64': {'key': '', 'type': 'bytearray', 'xml': {'name': 'source_if_none_match_crc64'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(SourceModifiedAccessConditions, self).__init__(**kwargs)
        self.source_if_match_crc64 = kwargs.get('source_if_match_crc64', None)
        self.source_if_none_match_crc64 = kwargs.get('source_if_none_match_crc64', None)


class StorageError(Model):
    """StorageError.

    :param message:
    :type message: str
    """

    _attribute_map = {
        'message': {'key': 'Message', 'type': 'str', 'xml': {'name': 'Message'}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(StorageError, self).__init__(**kwargs)
        self.message = kwargs.get('message', None)


class StorageErrorException(HttpResponseError):
    """Server responsed with exception of type: 'StorageError'.

    :param deserialize: A deserializer
    :param response: Server response to be deserialized.
    """

    def __init__(self, response, deserialize, *args):

      model_name = 'StorageError'
      self.error = deserialize(model_name, response)
      if self.error is None:
          self.error = deserialize.dependencies[model_name]()
      super(StorageErrorException, self).__init__(response=response)


class StorageServiceProperties(Model):
    """Storage service properties.

    :param hour_metrics: A summary of request statistics grouped by API in
     hourly aggregates for files.
    :type hour_metrics: ~azure.storage.fileshare.models.Metrics
    :param minute_metrics: A summary of request statistics grouped by API in
     minute aggregates for files.
    :type minute_metrics: ~azure.storage.fileshare.models.Metrics
    :param cors: The set of CORS rules.
    :type cors: list[~azure.storage.fileshare.models.CorsRule]
    """

    _attribute_map = {
        'hour_metrics': {'key': 'HourMetrics', 'type': 'Metrics', 'xml': {'name': 'HourMetrics'}},
        'minute_metrics': {'key': 'MinuteMetrics', 'type': 'Metrics', 'xml': {'name': 'MinuteMetrics'}},
        'cors': {'key': 'Cors', 'type': '[CorsRule]', 'xml': {'name': 'Cors', 'itemsName': 'CorsRule', 'wrapped': True}},
    }
    _xml_map = {
    }

    def __init__(self, **kwargs):
        super(StorageServiceProperties, self).__init__(**kwargs)
        self.hour_metrics = kwargs.get('hour_metrics', None)
        self.minute_metrics = kwargs.get('minute_metrics', None)
        self.cors = kwargs.get('cors', None)
