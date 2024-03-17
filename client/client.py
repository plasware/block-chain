import os
import json
import random
from socket import *
from time import sleep
from Transaction import Transaction

PATH = os.path.dirname(__file__)

LOCAL_IP = "192.168.42.1"

with open(PATH + "/private_key.txt", 'r') as f:
    PRIVATE_KEY = f.read()

ADDRESS = ('255.255.255.255', 10001)

SERVER_SOCKET = socket(AF_INET, SOCK_DGRAM)  # Use UDP to broadcast
SERVER_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

if __name__ == '__main__':
    while True:
        random_from_to = random.sample(range(10, 20), 2)
        from_ip = LOCAL_IP
        to_ip = "192.168.42." + str(random_from_to[1])
        value = round(random.uniform(1, 50), 2)

        transaction = Transaction(from_ip=from_ip, to_ip=to_ip, value=value)
        transaction.signature = transaction.sign_signature(PRIVATE_KEY)

        message = {'time_stamp': transaction.time_stamp, 'from_ip': transaction.from_ip, 'to_ip': transaction.to_ip,
                   'value': transaction.value, 'signature': transaction.signature}
        message_json = json.dumps(message)
        SERVER_SOCKET.sendto(message_json.encode('utf-8'), ADDRESS)
        print("Transaction Broadcast")

        sleep(5)
