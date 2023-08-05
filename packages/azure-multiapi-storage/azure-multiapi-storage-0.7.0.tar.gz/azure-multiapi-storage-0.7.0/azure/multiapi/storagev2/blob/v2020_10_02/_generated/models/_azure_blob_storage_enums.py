# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum, EnumMeta
from six import with_metaclass

class _CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(self, name):
        return super().__getitem__(name.upper())

    def __getattr__(cls, name):
        """Return the enum member matching `name`
        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.
        """
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name)


class AccessTier(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    P4 = "P4"
    P6 = "P6"
    P10 = "P10"
    P15 = "P15"
    P20 = "P20"
    P30 = "P30"
    P40 = "P40"
    P50 = "P50"
    P60 = "P60"
    P70 = "P70"
    P80 = "P80"
    HOT = "Hot"
    COOL = "Cool"
    ARCHIVE = "Archive"

class AccessTierOptional(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    P4 = "P4"
    P6 = "P6"
    P10 = "P10"
    P15 = "P15"
    P20 = "P20"
    P30 = "P30"
    P40 = "P40"
    P50 = "P50"
    P60 = "P60"
    P70 = "P70"
    P80 = "P80"
    HOT = "Hot"
    COOL = "Cool"
    ARCHIVE = "Archive"

class AccessTierRequired(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    P4 = "P4"
    P6 = "P6"
    P10 = "P10"
    P15 = "P15"
    P20 = "P20"
    P30 = "P30"
    P40 = "P40"
    P50 = "P50"
    P60 = "P60"
    P70 = "P70"
    P80 = "P80"
    HOT = "Hot"
    COOL = "Cool"
    ARCHIVE = "Archive"

class AccountKind(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    STORAGE = "Storage"
    BLOB_STORAGE = "BlobStorage"
    STORAGE_V2 = "StorageV2"
    FILE_STORAGE = "FileStorage"
    BLOCK_BLOB_STORAGE = "BlockBlobStorage"

class ArchiveStatus(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    REHYDRATE_PENDING_TO_HOT = "rehydrate-pending-to-hot"
    REHYDRATE_PENDING_TO_COOL = "rehydrate-pending-to-cool"

class BlobExpiryOptions(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    NEVER_EXPIRE = "NeverExpire"
    RELATIVE_TO_CREATION = "RelativeToCreation"
    RELATIVE_TO_NOW = "RelativeToNow"
    ABSOLUTE = "Absolute"

class BlobImmutabilityPolicyMode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    UNLOCKED = "Unlocked"
    LOCKED = "Locked"
    MUTABLE = "Mutable"

class BlobType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    BLOCK_BLOB = "BlockBlob"
    PAGE_BLOB = "PageBlob"
    APPEND_BLOB = "AppendBlob"

class BlockListType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    COMMITTED = "committed"
    UNCOMMITTED = "uncommitted"
    ALL = "all"

class CopyStatusType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    PENDING = "pending"
    SUCCESS = "success"
    ABORTED = "aborted"
    FAILED = "failed"

class DeleteSnapshotsOptionType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    INCLUDE = "include"
    ONLY = "only"

class EncryptionAlgorithmType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    NONE = "None"
    AES256 = "AES256"

class GeoReplicationStatusType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The status of the secondary location
    """

    LIVE = "live"
    BOOTSTRAP = "bootstrap"
    UNAVAILABLE = "unavailable"

class LeaseDurationType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    INFINITE = "infinite"
    FIXED = "fixed"

class LeaseStateType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    AVAILABLE = "available"
    LEASED = "leased"
    EXPIRED = "expired"
    BREAKING = "breaking"
    BROKEN = "broken"

class LeaseStatusType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    LOCKED = "locked"
    UNLOCKED = "unlocked"

class ListBlobsIncludeItem(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    COPY = "copy"
    DELETED = "deleted"
    METADATA = "metadata"
    SNAPSHOTS = "snapshots"
    UNCOMMITTEDBLOBS = "uncommittedblobs"
    VERSIONS = "versions"
    TAGS = "tags"
    IMMUTABILITYPOLICY = "immutabilitypolicy"
    LEGALHOLD = "legalhold"
    DELETEDWITHVERSIONS = "deletedwithversions"

class ListContainersIncludeType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    METADATA = "metadata"
    DELETED = "deleted"

class PathRenameMode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    LEGACY = "legacy"
    POSIX = "posix"

class PremiumPageBlobAccessTier(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    P4 = "P4"
    P6 = "P6"
    P10 = "P10"
    P15 = "P15"
    P20 = "P20"
    P30 = "P30"
    P40 = "P40"
    P50 = "P50"
    P60 = "P60"
    P70 = "P70"
    P80 = "P80"

class PublicAccessType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    CONTAINER = "container"
    BLOB = "blob"

class QueryFormatType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The quick query format type.
    """

    DELIMITED = "delimited"
    JSON = "json"
    ARROW = "arrow"
    PARQUET = "parquet"

class RehydratePriority(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """If an object is in rehydrate pending state then this header is returned with priority of
    rehydrate. Valid values are High and Standard.
    """

    HIGH = "High"
    STANDARD = "Standard"

class SequenceNumberActionType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    MAX = "max"
    UPDATE = "update"
    INCREMENT = "increment"

class SkuName(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    STANDARD_LRS = "Standard_LRS"
    STANDARD_GRS = "Standard_GRS"
    STANDARD_RAGRS = "Standard_RAGRS"
    STANDARD_ZRS = "Standard_ZRS"
    PREMIUM_LRS = "Premium_LRS"

class StorageErrorCode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Error codes returned by the service
    """

    ACCOUNT_ALREADY_EXISTS = "AccountAlreadyExists"
    ACCOUNT_BEING_CREATED = "AccountBeingCreated"
    ACCOUNT_IS_DISABLED = "AccountIsDisabled"
    AUTHENTICATION_FAILED = "AuthenticationFailed"
    AUTHORIZATION_FAILURE = "AuthorizationFailure"
    CONDITION_HEADERS_NOT_SUPPORTED = "ConditionHeadersNotSupported"
    CONDITION_NOT_MET = "ConditionNotMet"
    EMPTY_METADATA_KEY = "EmptyMetadataKey"
    INSUFFICIENT_ACCOUNT_PERMISSIONS = "InsufficientAccountPermissions"
    INTERNAL_ERROR = "InternalError"
    INVALID_AUTHENTICATION_INFO = "InvalidAuthenticationInfo"
    INVALID_HEADER_VALUE = "InvalidHeaderValue"
    INVALID_HTTP_VERB = "InvalidHttpVerb"
    INVALID_INPUT = "InvalidInput"
    INVALID_MD5 = "InvalidMd5"
    INVALID_METADATA = "InvalidMetadata"
    INVALID_QUERY_PARAMETER_VALUE = "InvalidQueryParameterValue"
    INVALID_RANGE = "InvalidRange"
    INVALID_RESOURCE_NAME = "InvalidResourceName"
    INVALID_URI = "InvalidUri"
    INVALID_XML_DOCUMENT = "InvalidXmlDocument"
    INVALID_XML_NODE_VALUE = "InvalidXmlNodeValue"
    MD5_MISMATCH = "Md5Mismatch"
    METADATA_TOO_LARGE = "MetadataTooLarge"
    MISSING_CONTENT_LENGTH_HEADER = "MissingContentLengthHeader"
    MISSING_REQUIRED_QUERY_PARAMETER = "MissingRequiredQueryParameter"
    MISSING_REQUIRED_HEADER = "MissingRequiredHeader"
    MISSING_REQUIRED_XML_NODE = "MissingRequiredXmlNode"
    MULTIPLE_CONDITION_HEADERS_NOT_SUPPORTED = "MultipleConditionHeadersNotSupported"
    OPERATION_TIMED_OUT = "OperationTimedOut"
    OUT_OF_RANGE_INPUT = "OutOfRangeInput"
    OUT_OF_RANGE_QUERY_PARAMETER_VALUE = "OutOfRangeQueryParameterValue"
    REQUEST_BODY_TOO_LARGE = "RequestBodyTooLarge"
    RESOURCE_TYPE_MISMATCH = "ResourceTypeMismatch"
    REQUEST_URL_FAILED_TO_PARSE = "RequestUrlFailedToParse"
    RESOURCE_ALREADY_EXISTS = "ResourceAlreadyExists"
    RESOURCE_NOT_FOUND = "ResourceNotFound"
    SERVER_BUSY = "ServerBusy"
    UNSUPPORTED_HEADER = "UnsupportedHeader"
    UNSUPPORTED_XML_NODE = "UnsupportedXmlNode"
    UNSUPPORTED_QUERY_PARAMETER = "UnsupportedQueryParameter"
    UNSUPPORTED_HTTP_VERB = "UnsupportedHttpVerb"
    APPEND_POSITION_CONDITION_NOT_MET = "AppendPositionConditionNotMet"
    BLOB_ALREADY_EXISTS = "BlobAlreadyExists"
    BLOB_IMMUTABLE_DUE_TO_POLICY = "BlobImmutableDueToPolicy"
    BLOB_NOT_FOUND = "BlobNotFound"
    BLOB_OVERWRITTEN = "BlobOverwritten"
    BLOB_TIER_INADEQUATE_FOR_CONTENT_LENGTH = "BlobTierInadequateForContentLength"
    BLOB_USES_CUSTOMER_SPECIFIED_ENCRYPTION = "BlobUsesCustomerSpecifiedEncryption"
    BLOCK_COUNT_EXCEEDS_LIMIT = "BlockCountExceedsLimit"
    BLOCK_LIST_TOO_LONG = "BlockListTooLong"
    CANNOT_CHANGE_TO_LOWER_TIER = "CannotChangeToLowerTier"
    CANNOT_VERIFY_COPY_SOURCE = "CannotVerifyCopySource"
    CONTAINER_ALREADY_EXISTS = "ContainerAlreadyExists"
    CONTAINER_BEING_DELETED = "ContainerBeingDeleted"
    CONTAINER_DISABLED = "ContainerDisabled"
    CONTAINER_NOT_FOUND = "ContainerNotFound"
    CONTENT_LENGTH_LARGER_THAN_TIER_LIMIT = "ContentLengthLargerThanTierLimit"
    COPY_ACROSS_ACCOUNTS_NOT_SUPPORTED = "CopyAcrossAccountsNotSupported"
    COPY_ID_MISMATCH = "CopyIdMismatch"
    FEATURE_VERSION_MISMATCH = "FeatureVersionMismatch"
    INCREMENTAL_COPY_BLOB_MISMATCH = "IncrementalCopyBlobMismatch"
    INCREMENTAL_COPY_OF_ERALIER_VERSION_SNAPSHOT_NOT_ALLOWED = "IncrementalCopyOfEralierVersionSnapshotNotAllowed"
    INCREMENTAL_COPY_SOURCE_MUST_BE_SNAPSHOT = "IncrementalCopySourceMustBeSnapshot"
    INFINITE_LEASE_DURATION_REQUIRED = "InfiniteLeaseDurationRequired"
    INVALID_BLOB_OR_BLOCK = "InvalidBlobOrBlock"
    INVALID_BLOB_TIER = "InvalidBlobTier"
    INVALID_BLOB_TYPE = "InvalidBlobType"
    INVALID_BLOCK_ID = "InvalidBlockId"
    INVALID_BLOCK_LIST = "InvalidBlockList"
    INVALID_OPERATION = "InvalidOperation"
    INVALID_PAGE_RANGE = "InvalidPageRange"
    INVALID_SOURCE_BLOB_TYPE = "InvalidSourceBlobType"
    INVALID_SOURCE_BLOB_URL = "InvalidSourceBlobUrl"
    INVALID_VERSION_FOR_PAGE_BLOB_OPERATION = "InvalidVersionForPageBlobOperation"
    LEASE_ALREADY_PRESENT = "LeaseAlreadyPresent"
    LEASE_ALREADY_BROKEN = "LeaseAlreadyBroken"
    LEASE_ID_MISMATCH_WITH_BLOB_OPERATION = "LeaseIdMismatchWithBlobOperation"
    LEASE_ID_MISMATCH_WITH_CONTAINER_OPERATION = "LeaseIdMismatchWithContainerOperation"
    LEASE_ID_MISMATCH_WITH_LEASE_OPERATION = "LeaseIdMismatchWithLeaseOperation"
    LEASE_ID_MISSING = "LeaseIdMissing"
    LEASE_IS_BREAKING_AND_CANNOT_BE_ACQUIRED = "LeaseIsBreakingAndCannotBeAcquired"
    LEASE_IS_BREAKING_AND_CANNOT_BE_CHANGED = "LeaseIsBreakingAndCannotBeChanged"
    LEASE_IS_BROKEN_AND_CANNOT_BE_RENEWED = "LeaseIsBrokenAndCannotBeRenewed"
    LEASE_LOST = "LeaseLost"
    LEASE_NOT_PRESENT_WITH_BLOB_OPERATION = "LeaseNotPresentWithBlobOperation"
    LEASE_NOT_PRESENT_WITH_CONTAINER_OPERATION = "LeaseNotPresentWithContainerOperation"
    LEASE_NOT_PRESENT_WITH_LEASE_OPERATION = "LeaseNotPresentWithLeaseOperation"
    MAX_BLOB_SIZE_CONDITION_NOT_MET = "MaxBlobSizeConditionNotMet"
    NO_AUTHENTICATION_INFORMATION = "NoAuthenticationInformation"
    NO_PENDING_COPY_OPERATION = "NoPendingCopyOperation"
    OPERATION_NOT_ALLOWED_ON_INCREMENTAL_COPY_BLOB = "OperationNotAllowedOnIncrementalCopyBlob"
    PENDING_COPY_OPERATION = "PendingCopyOperation"
    PREVIOUS_SNAPSHOT_CANNOT_BE_NEWER = "PreviousSnapshotCannotBeNewer"
    PREVIOUS_SNAPSHOT_NOT_FOUND = "PreviousSnapshotNotFound"
    PREVIOUS_SNAPSHOT_OPERATION_NOT_SUPPORTED = "PreviousSnapshotOperationNotSupported"
    SEQUENCE_NUMBER_CONDITION_NOT_MET = "SequenceNumberConditionNotMet"
    SEQUENCE_NUMBER_INCREMENT_TOO_LARGE = "SequenceNumberIncrementTooLarge"
    SNAPSHOT_COUNT_EXCEEDED = "SnapshotCountExceeded"
    SNAPHOT_OPERATION_RATE_EXCEEDED = "SnaphotOperationRateExceeded"
    SNAPSHOTS_PRESENT = "SnapshotsPresent"
    SOURCE_CONDITION_NOT_MET = "SourceConditionNotMet"
    SYSTEM_IN_USE = "SystemInUse"
    TARGET_CONDITION_NOT_MET = "TargetConditionNotMet"
    UNAUTHORIZED_BLOB_OVERWRITE = "UnauthorizedBlobOverwrite"
    BLOB_BEING_REHYDRATED = "BlobBeingRehydrated"
    BLOB_ARCHIVED = "BlobArchived"
    BLOB_NOT_ARCHIVED = "BlobNotArchived"
    AUTHORIZATION_SOURCE_IP_MISMATCH = "AuthorizationSourceIPMismatch"
    AUTHORIZATION_PROTOCOL_MISMATCH = "AuthorizationProtocolMismatch"
    AUTHORIZATION_PERMISSION_MISMATCH = "AuthorizationPermissionMismatch"
    AUTHORIZATION_SERVICE_MISMATCH = "AuthorizationServiceMismatch"
    AUTHORIZATION_RESOURCE_TYPE_MISMATCH = "AuthorizationResourceTypeMismatch"
