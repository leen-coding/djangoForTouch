from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    # 客户端向后端发送websocket请求时，并且服务端允许客户端创建链接，自动触发
    def websocket_connect(self, message):
        self.accept()  # 握手
        CONN_LIST.append(self)
        self.send(b'hello')
        # async_to_sync(self.channel_layer.group_add("IoT",self.channel_name))

    # 消息互通
    def websocket_receive(self, message):
        print(message['text'])
        for conn in CONN_LIST:
            conn.send(message['text'])
        # async_to_sync(self.channel_layer.group_send)("IoT",{"type":"xx.oo", 'message':message})

    # def xx_oo(self,event):
    #     text = event['message']['text']
    #     self.send(text)
    # 客户端主动断开链接自动触发。服务端通过self.close（）主动断开

    def websocket_disconnect(self, message):
        # async_to_sync(self.channel_layer.group_discard)("IoT", self.channel_name)
        CONN_LIST.remove(self)
        raise StopConsumer()
