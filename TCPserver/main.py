import socket
import time
import socket
import json
import threading
import pymongo
import logging
import datetime

logging.basicConfig(filename="tcp_server.log", level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
machine_id_to_socket = {}
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
print(mongo_client.server_info())  # 判断是否连接成功
mongo_db = mongo_client['TouchOperation']

mongo_collection = mongo_db['Touch2Server']
mongo_collection.delete_many({"machine_id":"TOUCH"})

def CalResult(buf, begin):
    # 1X-0.01152Y-0.11487Z+0.00000R-0.96818P-1.41146Y-0.12827
    Result = int(buf[(begin + 4)]) * 10000 + int(buf[(begin + 5)]) * 1000 + int(buf[(begin + 6)]) * 100 + int(
        buf[(begin + 7)]) * 10 + int(buf[(begin + 8)])

    Result = Result / 100000 + int(buf[(begin + 2)])

    if ((buf[(begin + 1)]) == '-'):
        Result = -Result

    return Result


def touch2server(data):
    info = {
        'machine_id': 'TOUCH',
        'data': data,
        'date': datetime.datetime.now()
    }
    mongo_collection.insert_one(info)



def server2dobot(client):
    # last_id = [i for i in mongo_collection.find({'name': 'TOUCH'}).sort('_id', -1).limit(1)][0]['data']
    last_data = [i for i in mongo_collection.find({'machine_id': 'TOUCH'}).sort('_id', -1).limit(1)][0]['data']

    print(last_data)
    last_data_bytes = bytes(last_data, encoding = "utf8")
    client.send(last_data_bytes)




def handle_request(address, client):
    logger.info(f'connection from {address} has been established!')
    while True:
        recv_data = client.recv(1024)

        if recv_data:
            machine_id = recv_data[:5].decode("utf-8")
            print(machine_id)
            if machine_id == "TOUCH":
                data = recv_data[5:68].decode("utf-8")
                touch2server(data)
            elif machine_id == "DOBOT":
                server2dobot(client)
            else:
                logger.warning(f'Unknown machine_id: {machine_id}')
                print(f'Unknown machine_id: {machine_id}')
        else:
            logger.info(f'connection from {address} has been stopped!')
            break

    client.close()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(('', 8888))
    s.listen(128)
    data_queue = []
    while True:
        client, address = s.accept()
        print(address)
        sub_thread = threading.Thread(target=handle_request, args=(address, client))
        sub_thread.start()
