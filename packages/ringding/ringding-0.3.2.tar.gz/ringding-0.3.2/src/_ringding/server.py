import dataclasses
import json
import logging
import time
from typing import cast, Dict, Callable, Any, Type

from _ringding.client.UnidentifiedClient import UnidentifiedClient
from _ringding.client.base import BaseClient
from _ringding.client.rdclient import RdClient

from _ringding.messages import Message, RESPONSE_TYPES, NotificationResponse
from _ringding.ws.wsserver import WebsocketServer
from ringding.datatypes import HandshakeError

CLIENT_FACTORY_IF = Callable[[object, Dict[str, Any]], BaseClient]


class _ApiEncoder(json.JSONEncoder):
    """Default JSON-encoder for sending API messages.."""

    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


class RdServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 36097,
                 log_level=logging.INFO):
        """
        Create a new RdServer instance.

        :param host: The host to listen to data, e.g. "localhost" or "192.168.0.123"
        :param port: The port to listen on.
        :param log_level: The log level (Any of logging.XYZ)
        """
        self._host = host
        self._port = port
        self._log_level = log_level
        self._server: WebsocketServer = cast(WebsocketServer, None)
        self._CLIENTS: Dict[int, BaseClient] = {}
        self._entrypoint = None
        self._is_started = False

    def serve(self, entrypoint: object):
        """
        Run the server and listen for messages

        :param entrypoint: The API root object. If you use a type here, each client
            will get its own instance of the API. If you hand in an object, all clients
            will share the same object. Use the latter one for public API's with
            non-client-related data, the first one for APIs that have only
            client-related data.
        """
        self._entrypoint = entrypoint

        self._server = WebsocketServer(self._port,
                                       host=self._host,
                                       loglevel=self._log_level)
        self._server.set_fn_new_client(self._on_client_connect)
        self._server.set_fn_client_left(self._on_client_disconnect)
        self._server.set_fn_message_received(self.on_message)
        self._is_started = True
        self._server.run_forever()

    def on_client_connect(self, client: BaseClient):
        pass

    def on_client_disconnect(self, client: BaseClient):
        pass

    def client_factory(self, entrypoint: None,
                       handshake_data: Dict[str, Any]) -> BaseClient:
        """
        Override to provide a client factory that can handle the authentication after
        a new client joined. With a client factory, you can make sure that only valid
        clients with a proper authentication can access the API. You can also
        return different APIs for different users.

        :param entrypoint: The entrypoint / The API
        :param handshake_data: The handshake data the client got.
        :return: A client based on RdClient.
        """
        return RdClient(entrypoint, handshake_data)

    def wait_until_started(self):
        """
        Will return after the server has been started. Use if you start the server
        in a thread.
        """
        while not self._is_started:
            time.sleep(0.2)
        time.sleep(0.2)  # Give run_forever some time to do what it needs to.

    def stop(self):
        """Stop the server."""
        self._is_started = False
        self._server.shutdown()

    def _on_client_connect(self, client_data: Dict[str, Any], server: WebsocketServer):
        """
        Called when a new client joins.

        :param client_data: A dictionary with client data (ID, URL)
        :param server: The underlying WebSocketServer
        """
        client = UnidentifiedClient(self._entrypoint, self.upgrade_client)
        client.connect_client(self, client_data)
        self._CLIENTS[client_data['id']] = client

    def _on_client_disconnect(self, client_data: Dict[str, Any], server: WebsocketServer):
        """
        :param client_data:
        :return:
        """
        self.on_client_disconnect(self._CLIENTS[client_data['id']])
        del self._CLIENTS[client_data['id']]

    def on_message(self, client_data: Dict, server: WebsocketServer, message: str):
        """
        Called when a new message arrives from any client.

        :param client_data: A dictionary with client data (ID, URL)
        :param server: The underlying WebSocketServer
        :param message: The message.
        """
        logging.debug(f'Server received message: {message}')
        client = self._CLIENTS.get(client_data['id'])
        data = Message(**json.loads(message))
        client.on_message(data)

    def upgrade_client(self, client_data: Dict, handshake_data: Dict):
        """
        Upgrade a client after the handshake is done. Replaces an UnidentifiedClient
        with a "real" client coming from the client factory.

        :param client_data: A dictionary with client data (ID, URL)
        :param handshake_data: The data transmitted during the handshake.
        """
        del self._CLIENTS[client_data['id']]
        try:
            client = self.client_factory(self._entrypoint, handshake_data)
        except Exception as error:
            raise HandshakeError(
                f'Handshake did not succeed: Error in client factory: {error}')
        if not isinstance(client, BaseClient):
            raise HandshakeError(
                f'Handshake did not succeed: Client factory did return invalid '
                f'client "{client}"')
        client.connect_client(self, client_data)
        self._CLIENTS[client_data['id']] = client
        self.on_client_connect(client)


    def notify(self, client: Dict, message: RESPONSE_TYPES):
        """
        Send a message to a single client.

        :param client: The client raw data
        :param message: The message object to send
        """
        self.send_raw_message(client, json.dumps(message, cls=self.get_json_encoder()))

    def broadcast(self, notification: NotificationResponse):
        """
        Broadcast a notification to all clients.

        :param notification: The notification that all clients shall receive.
        """
        raw_message = json.dumps(notification, cls=self.get_json_encoder())
        self._server.send_message_to_all(raw_message)

    def send_raw_message(self, client: Dict, message: str):
        """
        Send text to a client.

        :param client: The client raw data
        :param message: The text that the client shall receive.
        """
        self._server.send_message(client, message)

    def get_clients(self) -> Dict[int, BaseClient]:
        """
        Retrieve currently connected clients.
        The return value is a dictionary where each key is the identifier of a client.

        :return: An object with currently connected clients.
        """
        return self._CLIENTS

    def get_json_encoder(self) -> Type[json.JSONEncoder]:
        """
        Retrieve the JSON-encoder. Override to provide an own JSON-encoder.
        The JSON-Encoder must be able to convert dataclasses, e.g.

        class _ApiEncoder(json.JSONEncoder):
            def default(self, o: Any) -> Any:
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                return str(o)

        :return: The JSON encoder to convert returned objects to JSON.
        """
        return _ApiEncoder
