#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

import pkg_resources
from pkg_resources import DistributionNotFound
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse


try:
    distribution = pkg_resources.get_distribution('pyams-chat-ws')
except DistributionNotFound:
    distribution = None


class MonitorEndpoint(HTTPEndpoint):
    """Application monitoring endpoint"""

    async def get(self, request):
        """Default monitor endpoint"""
        return JSONResponse({
            'status': 'OK',
            'sessions_count': len(self.scope['app'].sessions),
            'server_version': distribution.version if distribution is not None else 'development'
        })
