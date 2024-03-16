"""
Client can call the functions to start or stop mining
"""
# TODO: A class for mining, including start/stop and checking the result
import hashlib
from Crypto.Hash import SHA256
from time import sleep
import json
from Transaction import Transaction
from Block import Block
from BlockChain import BlockChain
from Constant import DIFFICULTY

class Miner:
    def __init__(self,block,prev_hash,difficulty=DIFFICULTY):
        """
        Init the Miner Class
        Input:
            block: A class represents a generated block will be pow
            prev_hash: A str represents last block hash
            difficulty: A int represents the difficulty of work
        """
        self.block = block
        self.prev_hash = prev_hash
        self.difficulty = DIFFICULTY
        self.mining = False  
    
    # start mining
    def start_mining(self):
        """
        Start mining
     
        """
        if not self.mining:
            self.mining = True
            hash_result,nonce=self.pow()
            print(f"Found valid hash: {hash_result}, with nonce: {nonce}")
            return hash_result,nonce
        else:
            print("Mining is already in progress.")
        
    def pow(self):
        """
        Proof of work
        Input:
        Ouput:
            guess_hash: A str represents the hash result
            nonce: A str represents a random number
        """
        nonce = 0
        while True:
            transactionMessage = [str(i) for i in self.block.transactions]
            data = "".join(transactionMessage) + self.prev_hash + str(self.block.timestamp) + str(nonce)
            guess_hash = str(hashlib.sha256(data.encode('utf-8')).hexdigest())
            if guess_hash[:4] == "0000" :
                # print("mining nonce:",nonce)
                return guess_hash,nonce
            nonce += 1

if __name__ == "__main__":
    # Test
    block=Block(genesis_block=True)
    transaction1 = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
    transaction2 = Transaction(from_ip='192.168.42.11', to_ip='192.168.42.12', value=1.25)
    block2=Block([transaction1,transaction2],block,block.hash)
    miner = Miner(block2,block.hash)
    # 开始挖矿
    miner.start_mining()





