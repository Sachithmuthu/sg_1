from socketIO_client import SocketIO, BaseNamespace


class RBConnection(object):
    """ Class to connect to the ReadBridg animation server to send data.
        Attributes:
        name: Name of the sensor
        server:Name or IP address of server .
        port:Port address of server .
    """

    def __init__(self, name, server, port):
        self.socketIO = SocketIO(server, port)
        self.msg_namespace = self.socketIO.define(BaseNamespace, '/fromremote')
        self.msg_namespace.emit('sname', name)

    def send(self, data):
        """Send the data as JSON data to the server."""
        self.msg_namespace.emit('sensor_msg', data)

    def wait(self, options):
        """Wait the thread before exiting."""
        self.socketIO.wait(seconds=options)
