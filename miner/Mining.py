"""
Client can call the functions to start or stop mining
"""
# TODO: A class for mining, including start/stop and checking the result
import hashlib
from time import sleep
import json
from Transaction import Transaction
from Block import Block
from BlockChain import BlockChain

class Miner:
    def __init__(self,block,difficulty=4):
        """
        block: 区块
        difficulty: 难度值
        """
        self.block = block
        # 定义工作量难度，默认为4，表示有效的哈希值以4个“0”开始
        self.difficulty = difficulty
        self.mining = False  # 初始状态为未挖矿
    
    # 添加开始挖矿的方法
    def start_mining(self):
        if not self.mining:
            self.mining = True
            result=self.mine()
            print(result)
        else:
            print("Mining is already in progress.")

    # 添加停止挖矿的方法
    def stop_mining(self):
        if self.mining:
            self.mining = False
            print("Mining stopped.")
        else:
            print("Mining is not in progress.")
     
    @staticmethod
    def valid(last_proof,proof):
        """
        Validates the Proof
        """
        # 字符串拼接
        guess = (str(last_proof) + str(proof)).encode() 
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        
    def pow(self,last_proof):
        """
        power of work
        """
        proof = 0
        while self.valid(last_proof,proof) is False:
            proof += 1
        return proof


    def mine(self):
        # i = 0
        # prefix = '0'*self.difficulty
        blockchain = BlockChain()

        # 获取上一个block
        last_block = blockchain.getMaxHeightBlock()
        # 上一个block的哈希
        last_block_hash = last_block.hash
        # last_proof = last_block['proof']
        proof = self.pow(last_block_hash)

        # proof需要给Block，然后 proof 和 nonce 应该是一个意思

        new_transaction = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
        # 添加一个交易
        blockchain.addTransactionPool(new_transaction)
        # 创建一个区块
        mined_block = Block([new_transaction],last_block,last_block_hash,height=last_block.height+1,nonce=proof)
        blockchain.add_block(mined_block,mined_block.hash)
        print("-------挖到一个币-------")
        blockchain.getChainMessage()
        print("目前区块链是否合法：", blockchain.is_valid_chain())

        # if blockchain.is_valid_chain():
        #     current_height = mined_block.height
        #     longest_chain = len(blockchain)

        #     for existing_block in longest_chain:
        #         if existing_block.height == current_height:
        #             if mined_block.hash != existing_block.hash:
        #                 longest_chain_length = len(longest_chain)
        #                 if longest_chain_length < 2:
        #                     blockchain.add_block(mined_block,mined_block.hash)
        #                     print("-------挖到一个币-------")
        #                 else:
        #                     if mined_block.height > longest_chain[-2].height:
        #                         # blockchain.replace_chain(longest_chain[:-1] + [mined_block])
        #                         blockchain.add_block(mined_block,mined_block.hash)
        #                         print("-------挖到一个币-------")
        #                 break
        # else:
        #     return {"message": "Invalid blockchain"}
        
        response = {
            'message': "New Block Forged",
            'height': mined_block.height,
            'transactions': mined_block.transactions,
            'proof': mined_block.nonce,
            'previous_hash': mined_block.previousHash,
        }
        return response

if __name__ == "__main__":
    # Test
    miner = Miner(block=None, difficulty=4)
    # 开始挖矿
    miner.start_mining()
    
    # 模拟一段时间的挖矿过程
    sleep(10)
    
    # 停止挖矿
    miner.stop_mining()




