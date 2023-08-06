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

"""PyAMS_chat.message module

This message defines main chat message class.
"""

import json
from datetime import datetime, timezone
from json import JSONEncoder

from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

from pyams_chat.include import get_client
from pyams_chat.interfaces import IChatMessage, IChatMessageExtension, IChatMessageHandler
from pyams_security.interfaces.base import IPrincipalInfo
from pyams_security.utility import get_principal
from pyams_utils.adapter import get_adapter_weight


__docformat__ = 'restructuredtext'


@implementer(IChatMessage)
class ChatMessage:  # pylint: disable=too-many-instance-attributes
    """Chat message object"""

    host = FieldProperty(IChatMessage['host'])
    channel = FieldProperty(IChatMessage['channel'])
    action = FieldProperty(IChatMessage['action'])
    category = FieldProperty(IChatMessage['category'])
    status = FieldProperty(IChatMessage['status'])
    title = FieldProperty(IChatMessage['title'])
    message = FieldProperty(IChatMessage['message'])
    source = FieldProperty(IChatMessage['source'])
    target = FieldProperty(IChatMessage['target'])
    url = FieldProperty(IChatMessage['url'])
    timestamp = FieldProperty(IChatMessage['timestamp'])
    user_data = FieldProperty(IChatMessage['user_data'])

    @classmethod
    def create_empty_message(cls, request):
        """Create new empty message"""
        return ChatMessage(request,
                           action='',
                           category='',
                           title='',
                           message='')

    def __init__(self, request, **settings):
        self.request = request
        self.host = settings.pop('host', request.host_url)
        self.channel = settings.pop('channel',
                                    request.registry.settings.get('pyams_chat.channel_name'))
        self.context = settings.pop('context', request.context)
        self.action = settings.pop('action', None)
        self.category = settings.pop('category', None)
        self.status = settings.pop('status', 'info')
        self.title = settings.pop('title', None)
        self.message = settings.pop('message', None)
        source = settings.pop('source', None) or request.principal.id
        if IPrincipalInfo.providedBy(source):  # pylint: disable=no-value-for-parameter
            source = source.id
        self.source_id = source
        self.url = settings.pop('url', None)
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.user_data = settings

    def get_source(self, principal_id=None):
        """Get message source"""
        if principal_id is None:
            principal_id = self.request.principal.id
        principal = get_principal(self.request, principal_id)
        self.source = {
            'id': principal.id,
            'title': principal.title
        }
        for _adapter in sorted(
                self.request.registry.getAdapters((self,), IChatMessageExtension),
                key=get_adapter_weight):
            pass  # adapters should automatically extend current message
        # profile = IPublicProfile(principal)
        # if profile.avatar:
        #     self.source['avatar'] = absolute_url(profile.avatar, self.request,
        #                                          '++thumb++square:32x32.png')
        # configuration = IBackOfficeConfiguration(self.request.root)
        # self.title = '{0} - {1}'.format(configuration.short_title, principal.title)

    def get_target(self):
        """Get message target"""
        target = {}
        handler = self.request.registry.queryAdapter(self, IChatMessageHandler,
                                                     name=self.category)
        if handler is not None:
            target = handler.get_target()
        self.target = target

    def send(self):
        """Get message source and target and publish to Redis"""
        self.get_source(self.source_id)
        self.get_target()
        self.publish()

    def publish(self):
        """Convert message to JSON and publish to Redis channel"""
        client = getattr(self.request, 'redis_client', None)
        if client is None:
            client = get_client(self.request)
        if client is not None:
            json_data = json.dumps(self, cls=ChatMessageEncoder)
            client.publish(self.channel, json_data)


class ChatMessageEncoder(JSONEncoder):
    """Chat message encoder"""

    def default(self, obj):  # pylint: disable=arguments-renamed
        if isinstance(obj, ChatMessage):
            return {
                'host': obj.host,
                'channel': obj.channel,
                'action': obj.action,
                'category': obj.category,
                'status': obj.status,
                'title': obj.title,
                'message': obj.message,
                'source': obj.source,
                'target': obj.target,
                'url': obj.url,
                'timestamp': obj.timestamp
            }
        return super().default(obj)
