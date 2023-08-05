let _w3cWebSocket;
try {
    // Browser
    _w3cWebSocket = WebSocket
} catch (e) {
    // NodeJs
    _w3cWebSocket = require('websocket').w3cwebsocket;
}


MESSAGE_TYPE_ONESHOT = 0
MESSAGE_TYPE_REQUEST = 1
MESSAGE_TYPE_RESPONSE = 2
MESSAGE_TYPE_ERROR = 3
MESSAGE_TYPE_BROADCAST = 4


class _ringdingjs {
    /**
     * Connect to the backend. This is the first function you want to call. You want
     * to call it as least as possible, so ideally (for single page applications) one
     * time during the app initialization.
     * Can be awaited to continue after the connection has been established.
     * @param ws_url - URL for WebSocket backend, e.g. "ws://localhost:8001" or "wss://server.com:8001".
     * @param handshake_data - Additional data that can be used to perform a handshake on server side.
     * @param message_handler - Optional: A message handler that you can provide, e.g. for debugging. Will log the network communication.
     * @returns {Promise<null>}
     */
    connect = (ws_url, handshake_data, message_handler) => {
        if (message_handler) {
            this._logger = message_handler
        }
        this.ws_url = ws_url || this.ws_url
        this._logger('Connecting to ' + this.ws_url + '...')
        let resolver_function;
        let error_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            error_function = reject;
        })
        this._pending_promises['__wsopen__'] = {resolver_function, error_function}
        this._handshake_data = handshake_data || this._handshake_data
        this.ws = new this._wsBase(this.ws_url)
        this.ws.onopen = this._on_connect
        this.ws.onmessage = this._on_message
        this.ws.onerror = this._on_error
        this.ws.onclose = this._on_close
        return promise
    }

    /**
     * Disconnect from the server. Resets ringding.
     * Can be awaited to continue once cleanup is done.
     * @returns {Promise<null>}
     */
    disconnect = () => {
        let resolver_function;
        let error_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            error_function = reject;
        })
        this._pending_promises['__wsclose__'] = {resolver_function, error_function}
        this.ws.close()
        return promise
    }

    /**
     * Call a function on the backend and retrieve its return value.
     * @param cmd - The command string e.g. "MyApi.sum(*)"
     * @param parameters - The keyword arguments as dict.
     * @returns {Promise<any>} - Will return a promise that will contain the return value of the called function once resolved.
     */
    call = (cmd, parameters) => {
        let rdtrace = cmd.__rdtrace__;
        if (rdtrace !== undefined) {
            cmd = rdtrace[0].join('.')
            parameters = rdtrace[1]
        }
        const message = {
            cmd,
            type: MESSAGE_TYPE_REQUEST,
            id: this._get_id()
        }
        if (!parameters || Object.keys(parameters).length > 0) {
            message.param = parameters
        }
        let resolver_function;
        let reject_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            reject_function = reject;
        })
        this._pending_promises[message.id] = [resolver_function, reject_function]
        this._logger(">>> " + JSON.stringify(message))
        this.ws.send(JSON.stringify(message))
        return promise
    }

    /**
     * Call a function on the server. This does not give you any feedback on whether the call was successful or not.
     * @param cmd - The command string to call, e.g. "MyApi.sum(*)"
     * @param [parameters] - The keyword arguments as dict.
     */
    notify = (cmd, parameters) => {
        let rdtrace = cmd.__rdtrace__;
        if (rdtrace !== undefined) {
            cmd = rdtrace[0].join('.')
            parameters = rdtrace[1]
        }
        const message = {
            cmd,
            type: MESSAGE_TYPE_ONESHOT,
        }
        if (!parameters || Object.keys(parameters).length > 0) {
            message.param = parameters
        }
        this._logger(">>> " + JSON.stringify(message))
        this.ws.send(JSON.stringify(message))
    }

    /**
     * Register a callback to be called when an event is emitted by the server.
     *
     * @param event_id - The event identifier
     * @param callback - The callback to call. It receives the return value of that
     *                   emitted event as first parameter.
     */
    register_event = (event_id, callback) => {
        const registered_callbacks = this._registered_notifications[event_id] || []
        if (registered_callbacks.indexOf(callback) !== -1) {
            throw `The callback ${callback} on event ${event_id} cannot be registered twice!`
        }
        registered_callbacks.push(callback)
        this._registered_notifications[event_id] = registered_callbacks
    }

    /**
     * Unregister a registered event.
     * @param event_id - The event identifier
     * @param callback - The callback that has been used during registration.
     */
    unregister_event = (event_id, callback) => {
        const index = this._registered_notifications[event_id].indexOf(callback)
        if (index !== -1) {
            this._registered_notifications[event_id].splice(index, 1)
        }
        if (this._registered_notifications[event_id].length === 0) {
            delete this._registered_notifications[event_id]
        }
    }

    /**
     * Await an event. The resolved promise will contain the event data.
     *
     * Example: const timestamp = await RD.wait_for_event("next_timestamp")
     *
     * @param event_id - The event id.
     * @returns {Promise<any>} - The Promise which will return the event data during resolve.
     */
    wait_for_event = async (event_id) => {
        let resolve_function;
        let reject_function;
        const promise = new Promise(
            (resolve, reject) => {
                resolve_function = resolve;
                reject_function = reject
            })

        this._pending_promises[event_id] = [resolve_function, reject_function]

        return promise
    }

    constructor() {
        this._set_defaults()
    }

    /** Extract the initialization into a separate method to make the cleanup after
     * closing the socket easier.
     * @private
     */
    _set_defaults = () => {
        this.ws = null
        this.ws_url = 'ws://localhost:36097'
        this._handshake_data = {}
        this._wsBase = _w3cWebSocket
        this._logger = this._empty_logger
        this._pending_promises = {}
        this._next_id = -1
        this._registered_notifications = {}
    }

    /**
     * This obviously doesn't log anything but is used as a dummy method that is called
     * during logging.
     * @private
     */
    _empty_logger = () => {
    }

    /**
     * Return an ID unique in this session. Used to identify messages.
     * @returns number
     * @private
     */
    _get_id = () => {
        const next_id = this._next_id + 1
        this._next_id = next_id
        return next_id
    }

    _on_connect = async () => {
        const {resolver_function, error_function} = this._pending_promises['__wsopen__']
        delete this._pending_promises['__wsopen__']
        try {
            await this.call('handshake', this._handshake_data)
            resolver_function()
        } catch (e) {
            error_function(e)
        }
    }

    _on_error = (error) => {
        this._logger('Could not connect, an error occured: ', error)
        this._pending_promises['__wsopen__'].error_function()
        delete this._pending_promises['__wsopen__']
        setTimeout(this.connect, 3000)
    }

    _on_message = (messageEvent) => {
        this._logger('<<< ' + messageEvent.data)
        const message = JSON.parse(messageEvent.data)
        let pending_promises;
        if (message.type === MESSAGE_TYPE_ONESHOT) {
            const event_handlers = this._registered_notifications[message.cmd]
            if (event_handlers !== undefined) {
                for (let event_handler of event_handlers) {
                    event_handler(message.data)
                }
            }
            pending_promises = this._pending_promises[message.cmd]
            delete this._pending_promises[message.cmd]
        } else {
            pending_promises = this._pending_promises[message.id]
            delete this._pending_promises[message.id]
        }
        if (pending_promises !== undefined) {
            const [resolve, reject] = pending_promises
            if (message.type === MESSAGE_TYPE_ERROR) {
                reject(message.error)
            } else if (resolve) {
                resolve(message.data)
            }
        }
    }

    _on_close = () => {
        const resolver_function = this._pending_promises['__wsclose__'].resolver_function
        delete this._pending_promises['__wsclose__']
        this._set_defaults()
        resolver_function()
    }
}


function _empty_function() {
}

/**
 * This function will return an ApiProxy which is an object that emulates API calls.
 * It "remembers" the chain of the attributes that has been accessed and fires an actual
 * API call when the final method is called.
 * It has to be wrapped in an own function to make it possible that each CallApi() returns
 * an independent ApiProxy that does not interfear with others.
 * @private
 */
function _get_api_proxy() {
    const access_list = []
    const _ApiProxy = {
        get: function (target, prop) {
            access_list.push(prop)
            return new Proxy(_empty_function, _ApiProxy)
        },
        apply: function (target, thisarg, argumentslist) {
            let command = access_list.join('.')
            let parameters = {}
            if (argumentslist.length > 0) {
                command += '(*)'
                parameters = argumentslist[0]
            } else {
                command += '()'
            }
            return RD.call(command, parameters)
        },
        has: function () {
            return true
        }
    }
    return _ApiProxy
}


// For Browser
const RD = new _ringdingjs()
const CallApi = function () {
    return new Proxy(_empty_function, _get_api_proxy())
}

// For NodeJS
try {
    module.exports = {
        RD: RD,
        CallApi: CallApi
    }
} catch (error) {
    // No NodeJS environment (e.g. Browser environment)
}
