# from socketIO_client import SocketIO, BaseNamespace


# class MsgNamespace(BaseNamespace):

#     def on_stat_response(self, *args):
#         print('on_stat_response', args)


# socketIO = SocketIO('localhost', 3000)
# msg_namespace = socketIO.define(BaseNamespace, '/fromremote')

# msg_namespace.emit('sensor_msg', {'sensor': 1, 'activity': 6})
# socketIO.wait(seconds=10)


from RBConnection import RBConnection


con = RBConnection('S1', 'localhost', 3000)
con.send({'sensor': 1, 'activity': 6})
con.wait(2)
