from typing import Dict, Union, Type, Optional, Any, TYPE_CHECKING

from _ringding.messages import (ErrorResponse, Message, RESPONSE_TYPES)

if TYPE_CHECKING:
    from _ringding.server import RdServer


class _ApiEntry:
    """Proxy object for API entrypoint."""
    pass


class BaseClient:
    """
    The Client base.

    All clients must derive from this class. It provides the interface and base
    functionality of one client. The server will call the functions of this client
    when receiving messages.
    """

    def __init__(self, entry_point: Union[object, Type[object]],
                 handshake_data: Dict[str, Any]):
        """
        :param entry_point: The root object that defines the first level of the API.
            If you provide an initialized object, all clients will share the same
            instance. The data this instance holds will be shared among all clients.
            If you provide a type (an uninitialized class), the object will be
            instantiated by each client. So each client will have its own instance of
            that object.
        :param handshake_data: The data that was provided by the client during the
            handshake.
        """

        api_entry = _ApiEntry()
        initialized_entrypoint = entry_point
        if type(entry_point) == type:
            initialized_entrypoint = entry_point()
        api_entry.__dict__ = {
            initialized_entrypoint.__class__.__name__: initialized_entrypoint}
        self._api_entry = api_entry
        self._client_data: Dict = {}
        self._server: Optional['RdServer'] = None
        self._handshake_data = handshake_data

    def get_server(self) -> 'RdServer':
        """Return the RdServer that spawned this client."""
        return self._server

    def notify(self, message: RESPONSE_TYPES):
        """
        Send a message to the client.

        :param message: The message to send
        """
        try:
            self._server.notify(self._client_data, message)
        except Exception as error:
            self._server.notify(self._client_data,
                                ErrorResponse(message.id, str(error)))

    def on_message(self, message: Message):
        """
        Override to react on a specific message that was sent to this client.

        :param message: The message
        """
        pass

    def connect_client(self, server: 'RdServer', client_data: Dict):
        """
        Initialize the client. This method is called by the server to provide the
        server object and specific client data (e.g. the IP)

        :param server: The WebsocketServer
        :param client_data: A dictionary with client data.
        """
        self._client_data = client_data
        self._server = server

    def get_handshake_data(self) -> Dict[str, Any]:
        """
        Retrieve the data transmitted during handshake by the client.

        :return: The handshake data
        """
        return self._handshake_data
