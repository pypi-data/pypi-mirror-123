# -------------------------------------------------------------------------
# Copyright (c) Microsoft.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

from ..common.sharedaccesssignature import (
    SharedAccessSignature,
    _SharedAccessHelper,
)
from ._constants import X_MS_VERSION


class QueueSharedAccessSignature(SharedAccessSignature):
    '''
    Provides a factory for creating queue shares access
    signature tokens with a common account name and account key.  Users can either
    use the factory or can construct the appropriate service and use the
    generate_*_shared_access_signature method directly.
    '''

    def __init__(self, account_name, account_key):
        '''
        :param str account_name:
            The storage account name used to generate the shared access signatures.
        :param str account_key:
            The access key to generate the shares access signatures.
        '''
        super(QueueSharedAccessSignature, self).__init__(account_name, account_key, x_ms_version=X_MS_VERSION)

    def generate_queue(self, queue_name, permission=None,
                       expiry=None, start=None, id=None,
                       ip=None, protocol=None):
        '''
        Generates a shared access signature for the queue.
        Use the returned signature with the sas_token parameter of QueueService.

        :param str queue_name:
            Name of queue.
        :param QueuePermissions permission:
            The permissions associated with the shared access signature. The
            user is restricted to operations allowed by the permissions.
            Permissions must be ordered read, add, update, process.
            Required unless an id is given referencing a stored access policy
            which contains this field. This field must be omitted if it has been
            specified in an associated stored access policy.
        :param expiry:
            The time at which the shared access signature becomes invalid.
            Required unless an id is given referencing a stored access policy
            which contains this field. This field must be omitted if it has
            been specified in an associated stored access policy. Azure will always
            convert values to UTC. If a date is passed in without timezone info, it
            is assumed to be UTC.
        :type expiry: datetime or str
        :param start:
            The time at which the shared access signature becomes valid. If
            omitted, start time for this call is assumed to be the time when the
            storage service receives the request. Azure will always convert values
            to UTC. If a date is passed in without timezone info, it is assumed to
            be UTC.
        :type start: datetime or str
        :param str id:
            A unique value up to 64 characters in length that correlates to a
            stored access policy. To create a stored access policy, use
            set_blob_service_properties.
        :param str ip:
            Specifies an IP address or a range of IP addresses from which to accept requests.
            If the IP address from which the request originates does not match the IP address
            or address range specified on the SAS token, the request is not authenticated.
            For example, specifying sip=168.1.5.65 or sip=168.1.5.60-168.1.5.70 on the SAS
            restricts the request to those IP addresses.
        :param str protocol:
            Specifies the protocol permitted for a request made. The default value
            is https,http. See :class:`~azure.storage.common.models.Protocol` for possible values.
        '''
        sas = _SharedAccessHelper()
        sas.add_base(permission, expiry, start, ip, protocol, self.x_ms_version)
        sas.add_id(id)
        sas.add_resource_signature(self.account_name, self.account_key, 'queue', queue_name)

        return sas.get_token()
