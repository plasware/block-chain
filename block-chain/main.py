# TODO: 3 Threads(do mining-package, receive transaction, receive block from other nodes)

import threading
import time
import requests
import json
import hashlib
import random
import string
import os
import sys
import datetime
from Constant import *
from Database import TransactionDB, BlockChainDB, Addr2PublicKeyDB, AccountBookDB
from Block import Block
from Transaction import Transaction
from BlockChain import BlockChain
from Mining import Miner
from socket import *
from utils import common
from write_log import write_log


blockchainDB = BlockChainDB()
blockchain = blockchainDB.read()

accountBookDB = AccountBookDB()

ADDRESS = ('255.255.255.255', 10000)

BLOCK_SOCKET = socket(AF_INET, SOCK_DGRAM)  # Use UDP to broadcast
BLOCK_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
BLOCK_SOCKET.bind(('', 10000))

TRANSACTION_SOCKET = socket(AF_INET, SOCK_DGRAM)  # Use UDP to broadcast
TRANSACTION_SOCKET.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
TRANSACTION_SOCKET.bind(('', 10001))


# 1. Mining thread

def broadcast_new_block(new_block):
    """
    Broadcast the new block to other nodes
    Input:
        new_block: A Block object
    Output:
        None
    """
    message = new_block.getBlockSendMessage()
    message_json = json.dumps(message)
    BLOCK_SOCKET.sendto(message_json.encode('utf-8'), ADDRESS)


def mining_thread(block, prev_hash):
    """
    Mining thread
    """
    miner = Miner(block, prev_hash)
    hash_result, nonce = miner.start_mining()
    block.nonce = nonce
    # block.hash = hash_result
    broadcast_new_block(block)
    print('broadcasted new block')
    write_log('broadcasted new block')
    


# 2. Receive transaction thread

def receive_transaction_thread():
    """
    Receive transaction thread
    """
    while True:
        data, addr = TRANSACTION_SOCKET.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        transaction = Transaction(from_ip=message['from_ip'], to_ip=message['to_ip'], value=message['value'],
                                  signature=message['signature'], time_stamp=message['time_stamp'])
        publicDB = Addr2PublicKeyDB()
        publicKeyInfo = publicDB.read()
        public_key = publicKeyInfo[transaction.from_ip]
        if transaction.check_signature(public_key):
            transaction_db = TransactionDB()
            transactions = transaction_db.read()
            print(type(transactions))
            # write_log(type(transactions))
            transactions.append(transaction)
            print(len(transactions))
            # write_log(len(transactions))
            if common.checkTransactions(transactions):
                transaction_db.write(transactions)
                if len(transactions) == TRANSACTION_POOL_SIZE:
                    # Generate a new block
                    new_block = Block(transactions=transaction_db.read(),
                                      previousHash=blockchain.getMaxHeightBlock().hash,
                                      parent=blockchain.getMaxHeightBlock())
                    # Start mining
                    mining_thread_instance = threading.Thread(target=mining_thread,
                                                              args=(new_block, blockchain.getMaxHeightBlock().hash))
                    mining_thread_instance.start()
                print("Transaction received")
                write_log("Transaction received")
            else:
                print("Invalid transaction value")
                write_log("Invalid transaction value")
        else:
            print("Invalid transaction signature")
            write_log("Invalid transaction signature")
        # print(blockchain.transactions)
        time.sleep(5)


# 3. Receive block thread

def receive_block_thread():
    """
    Receive block thread
    """
    while True:
        data, addr = BLOCK_SOCKET.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        transactions = []
        for msg in message['transactions']:
            transaction = Transaction('', '', '')
            transaction.from_dict(msg)
            # print(msg, str(transaction))
            transactions.append(transaction)
        new_block = Block(transactions=transactions, previousHash=message['previousHash'],
                          time_stamp=message['timestamp'], nonce=message['nonce'],
                          parent=blockchain.getMaxHeightBlock())
        print(new_block.getBlockMessage())
        write_log(new_block.getBlockMessage())
        print('receive block message:', message)
        write_log(message)
        if blockchain.add_block(new_block):
            common.updateAccountBook(new_block.transactions)
            TransactionDB().write([])
            accountInfo = accountBookDB.read()
            accountInfo[addr[0]] += REWARD
            print("Block received")
            write_log("Block received")
            blockchainDB.write(blockchain)


# 4. Main function

def main():
    """
    Main function
    """
    TransactionDB().write([])
    receive_transaction_thread_instance = threading.Thread(target=receive_transaction_thread)
    receive_block_thread_instance = threading.Thread(target=receive_block_thread)
    receive_transaction_thread_instance.start()
    receive_block_thread_instance.start()


if __name__ == '__main__':
    main()
