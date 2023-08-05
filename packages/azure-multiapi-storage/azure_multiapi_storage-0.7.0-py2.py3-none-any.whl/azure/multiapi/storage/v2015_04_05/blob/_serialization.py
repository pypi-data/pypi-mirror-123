﻿#-------------------------------------------------------------------------
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
#--------------------------------------------------------------------------
from xml.sax.saxutils import escape as xml_escape
try:
    from xml.etree import cElementTree as ETree
except ImportError:
    from xml.etree import ElementTree as ETree
from .._common_conversion import (
    _encode_base64,
    _str,
)
from .._error import (
    _validate_not_none,
    _ERROR_START_END_NEEDED_FOR_MD5,
    _ERROR_RANGE_TOO_LARGE_FOR_MD5,
)
from ._error import (
    _ERROR_PAGE_BLOB_START_ALIGNMENT,
    _ERROR_PAGE_BLOB_END_ALIGNMENT,
    _ERROR_INVALID_BLOCK_ID,
)
import sys
if sys.version_info >= (3,):
    from io import BytesIO
else:
    from cStringIO import StringIO as BytesIO

def _get_path(container_name=None, blob_name=None):
    '''
    Creates the path to access a blob resource.

    container_name:
        Name of container.
    blob_name:
        The path to the blob.
    '''
    if container_name and blob_name:
        return '/{0}/{1}'.format(
            _str(container_name),
            _str(blob_name))
    elif container_name:
        return '/{0}'.format(_str(container_name))
    else:
        return '/'

def _validate_and_format_range_headers(request, start_range, end_range, start_range_required=True, end_range_required=True, check_content_md5=False, align_to_page=False):
    request.headers = request.headers or []
    if start_range_required == True:
        _validate_not_none('start_range', start_range)
    if end_range_required == True:
        _validate_not_none('end_range', end_range)
    _validate_page_ranges(start_range, end_range, align_to_page)
    if end_range is not None:
        request.headers.append(('x-ms-range', "bytes={0}-{1}".format(start_range, end_range)))
    else:
        request.headers.append(('x-ms-range', "bytes={0}-".format(start_range)))

    if check_content_md5 == True:
        if start_range is None or end_range is None:
            raise ValueError(_ERROR_START_END_NEEDED_FOR_MD5)
        if end_range - start_range > 4 * 1024 * 1024:
            raise ValueError(_ERROR_RANGE_TOO_LARGE_FOR_MD5)

        request.headers.append(('x-ms-range-get-content-md5', 'true'))

def _validate_page_ranges(start_range, end_range, align_to_page):
    if align_to_page == True:
        if start_range is not None and start_range % 512 != 0:
            raise ValueError(_ERROR_PAGE_BLOB_START_ALIGNMENT)
        if end_range is not None and end_range % 512 != 511:
            raise ValueError(_ERROR_PAGE_BLOB_END_ALIGNMENT)

def _convert_block_list_to_xml(block_id_list):
    '''
    <?xml version="1.0" encoding="utf-8"?>
    <BlockList>
      <Committed>first-base64-encoded-block-id</Committed>
      <Uncommitted>second-base64-encoded-block-id</Uncommitted>
      <Latest>third-base64-encoded-block-id</Latest>
    </BlockList>

    Convert a block list to xml to send.

    block_id_list:
        A list of BlobBlock containing the block ids and block state that are used in put_block_list.
    Only get block from latest blocks.
    '''
    if block_id_list is None:
        return ''

    block_list_element = ETree.Element('BlockList');
    
    # Enabled
    for block in block_id_list:
        if block.id is None:
            raise ValueError(_ERROR_INVALID_BLOCK_ID)
        id = xml_escape(_str(format(_encode_base64(block.id))))
        ETree.SubElement(block_list_element, block.state).text = id

    # Add xml declaration and serialize
    try:
        stream = BytesIO()
        ETree.ElementTree(block_list_element).write(stream, xml_declaration=True, encoding='utf-8', method='xml')
    except:
        raise
    finally:
        output = stream.getvalue()
        stream.close()
    
    # return xml value
    return output
