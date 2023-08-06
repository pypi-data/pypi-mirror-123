/* global MyAMS */

'use strict';


if (window.$ === undefined) {
    window.$ = MyAMS.$;
}


const chat = {

    unloadHandler: null,
    wsClient: null,
    accessToken: null,
    refreshToken: null,
    checkInterval: null,

    /**
     * Module initialization
     */
    initChat: () => {
        chat.openConnection();
    },

    /**
     * Open WebSocket connection
     */
    openConnection: () => {
        const
            notifications = $('#user-notifications'),
            wsEndpoint = notifications.data('ams-notifications-endpoint');
        if (wsEndpoint) {
            // Get authentication token
            MyAMS.require('ajax', 'notifications')
                .then(() => {
                    MyAMS.ajax.get(`${notifications.data('ams-jwt-verify-route')}`)
                        .then((result) => {
                            if (result.status === 'success') {
                                chat.accessToken = result.accessToken;
                                chat.refreshToken = result.refreshToken;
                                chat.wsClient = new WebSocket(wsEndpoint,
                                    ['accessToken', chat.accessToken]);
                                chat.wsClient.onopen = chat.onOpened;
                                chat.wsClient.onmessage = chat.onMessage;
                                chat.wsClient.onclose = chat.onClosed;
                                chat.checkInterval = setInterval(chat.checkConnection, 30000);
                            }
                        });
                });
        }
    },

    /**
     * Check WebSocket connection on periodic interval
     */
    checkConnection: () => {
        if ((chat.wsClient === null) || (chat.wsClient.readyState === WebSocket.CLOSED)) {
            chat.openConnection();
        }
    },

    /**
     * Event on opened WebSocket
     */
    onOpened: (evt) => {
        console.debug("WS opened", evt);
    },

    /**
     * Get message from WebSocket
     */
    onMessage: (evt) => {
        let message = evt.data;
        if (typeof message === 'string') {
            message = JSON.parse(message);
        }
        chat.showDesktopNotification(message);
    },

    /**
     * Show desktop notification
     */
    showDesktopNotification: (message) => {

        const checkNotificationPromise = () => {
            try {
                Notification.requestPermission().then();
            } catch (e) {
                return false
            }
            return true;
        };

        const do_notify = () => {
            const
                options = {
                    title: message.title,
                    body: message.message,
                    icon: message.source.avatar
                },
                notification = new Notification(options.title, options);
            if (message.url) {
                notification.onclick = () => {
                    window.open(message.url);
                };
            }
        };

        if (!('Notification' in window)) {
            console.debug("Notifications are not supported by this browser!");
        } else if (Notification.permission !== 'denied') {
            if (Notification.permission === 'default') {
                if (checkNotificationPromise()) {
                    Notification.requestPermission().then((permission) => {
                        if (permission === 'granted') {
                            do_notify();
                        }
                    });
                } else {
                    Notification.requestPermission((permission) => {
                        if (permission === 'granted') {
                            do_notify();
                        }
                    });
                }
            } else {
                do_notify();
            }
        }
    },

    /**
     * Event on closed WebSocket
     */
    onClosed: (evt) => {
        chat.wsClient = null;
        console.debug("WS closed !!!", evt);
    }
};


if (window.MyAMS) {
    MyAMS.config.modules.push('myams_chat');
    MyAMS.chat = chat;
    console.debug("MyAMS: chat module loaded...");
}
