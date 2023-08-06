==================
PyAMS chat package
==================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

It allows to send notifications through websockets to connected users, using a Redis server and
a *pubsub* subscriber as defined by PyAMS_chat_WS package.

    >>> import pprint
    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'
    >>> config.registry.settings['pyams_chat.channel_name'] = 'chat:main'

    >>> from beaker.cache import CacheManager, cache_regions
    >>> cache = CacheManager(**{'cache.type': 'memory'})
    >>> cache_regions.update({'short': {'type': 'memory', 'expire': 0}})
    >>> cache_regions.update({'long': {'type': 'memory', 'expire': 0}})

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_chat import includeme as include_chat
    >>> include_chat(config)

    >>> import transaction

    >>> from pyams_site.generations import upgrade_site
    >>> request = DummyRequest()

    >>> from pyramid.threadlocal import manager
    >>> manager.push({'request': request, 'registry': config.registry})

    >>> app = upgrade_site(request)
    Upgrading PyAMS security to generation 2...

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyams_utils.registry import handle_site_before_traverse
    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))


Chat messages
-------------

The base of this package usage is to create and send messages:

    >>> from pyams_security.principal import PrincipalInfo
    >>> from pyams_chat.include import client_from_config
    >>> from pyams_chat.message import ChatMessage

    >>> request.principal = PrincipalInfo(id='system:admin')
    >>> request.redis_client = client_from_config(config.registry.settings)

    >>> message = ChatMessage(request=request,
    ...                       action='notify',
    ...                       category='pyams.test',
    ...                       source=request.principal.id,
    ...                       title="Test message",
    ...                       message="Test message content")
    >>> message.send()

    >>> transaction.commit()


Chat messaging API
------------------

A REST API is available to get chat context; this context is used to filter chat messages:

    >>> from pyams_chat.api import get_chat_context
    >>> pprint.pprint(get_chat_context(request))
    {'context': {'*': ['user.login']},
     'principal': {'id': 'system:admin',
                   'principals': ('system.Everyone',),
                   'title': '__unknown__'},
     'status': 'success'}

We can also get chat messages:

    >>> from pyams_chat.api import get_notifications
    >>> pprint.pprint(get_notifications(request))
    {'notifications': [], 'timestamp': ...}

The notifications list is actually empty because the Redis list is filled by the websocket
server only when notifications are actually dispatched.

    >>> with request.redis_client as redis:
    ...     redis.lrange(f'chat:notifications::{request.host_url}', 0, -1)
    []

We can simulate this:

    >>> import json
    >>> from pyams_chat.message import ChatMessageEncoder

    >>> with request.redis_client as redis:
    ...     redis.lpush(f'chat:notifications::{request.host_url}',
    ...                 json.dumps(message, cls=ChatMessageEncoder))
    1

    >>> pprint.pprint(get_notifications(request))
    {'notifications': [], 'timestamp': ...}

We still get an empty notifications list because a message sender doesn't receive it's
own notifications:

    >>> request.principal = PrincipalInfo(id='test:user')
    >>> pprint.pprint(get_notifications(request))
    {'notifications': [], 'timestamp': ...}

Why is it still empty? That's because we have to define a *target* for a message, which is
a set of principals which should receive the message. These targets are defined by using a
named adapter, whose name must be the *category* of the message:

    >>> from pyams_utils.testing import call_decorator
    >>> from pyams_utils.adapter import adapter_config
    >>> from pyams_utils.adapter import ContextAdapter
    >>> from pyams_chat.interfaces import IChatMessage, IChatMessageHandler

    >>> class TestMessageHandler(ContextAdapter):
    ...
    ...     def get_target(self):
    ...         return {
    ...             'principals': ['test:user']
    ...     }

    >>> call_decorator(config, adapter_config, TestMessageHandler, name='pyams.test',
    ...                required=(IChatMessage, ), provides=IChatMessageHandler)

    >>> message.send()
    >>> with request.redis_client as redis:
    ...     redis.lpush(f'chat:notifications::{request.host_url}',
    ...                 json.dumps(message, cls=ChatMessageEncoder))
    2
    >>> pprint.pprint(get_notifications(request))
    {'notifications': [{'action': 'notify',
                        'category': 'pyams.test',
                        'channel': 'chat:main',
                        'host': 'http://example.com',
                        'message': 'Test message content',
                        'source': {'id': 'system:admin',
                                   'title': 'System manager authentication'},
                        'status': 'info',
                        'target': {'principals': ['test:user']},
                        'timestamp': '...T...',
                        'title': 'Test message',
                        'url': None}],
     'timestamp': ...}

A default message handler is available on user login:

    >>> from pyams_security.interfaces import AuthenticatedPrincipalEvent

    >>> request.principal = PrincipalInfo(id='system:admin')
    >>> event = AuthenticatedPrincipalEvent('admin', 'test:user')

    >>> from pyams_chat.handler.login import handle_authenticated_principal
    >>> handle_authenticated_principal(event)

    >>> message = ChatMessage(request=request,
    ...                       action='notify',
    ...                       category='user.login',
    ...                       source=request.principal.id,
    ...                       title="User login",
    ...                       message="{} logged in...".format(request.principal.title))
    >>> message.send()
    >>> with request.redis_client as redis:
    ...     redis.lpush(f'chat:notifications::{request.host_url}',
    ...                 json.dumps(message, cls=ChatMessageEncoder))
    3
    >>> pprint.pprint(get_notifications(request))
    {'notifications': [{'action': 'notify',
                        'category': 'user.login',
                        'channel': 'chat:main',
                        'host': 'http://example.com',
                        'message': '__unknown__ logged in...',
                        'source': {'id': 'system:admin',
                                   'title': 'System manager authentication'},
                        'status': 'info',
                        'target': {'principals': ['system:admin']},
                        'timestamp': '...T...',
                        'title': 'User login',
                        'url': None}],
     'timestamp': ...}


    >>> tearDown()
