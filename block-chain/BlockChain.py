from Transaction import Transaction

from Block import Block
from Constant import DIFFICULTY, MAX_BRANCH_LEN_DIFF
from utils.common import checkTransactions
import copy
from write_log import write_log

class BlockChain:
    def __init__(self):
        """
        init a block chain
        """
        self.blockchain = dict({})
        genesis_block = self.genesisBlock()
        self.maxheightnode = genesis_block
        self.genesis = genesis_block
        self.blockchain[genesis_block.hash] = genesis_block
        self.transactions = []

    # 祖先区块
    def genesisBlock(self):
        """
        create a genesis block
        :return: a genesis block
        """
        block = Block(genesis_block=True)
        return block

    def add_block(self, block=None, proof=None):
        """
        add a block to block chain
        :param block: the block need to add
        :param proof: the hash of block
        :return: True or False
        """
        prev_hash = block.previousHash
        # If the hash value of the previous block is empty, False is returned
        if prev_hash == None:
            print("Block not valid because previous block hash is None")
            write_log("Block not valid because previous block hash is None")
            return False
        # If the hash of the previous block is not in the blockchain, False is returned
        if prev_hash not in self.blockchain:
            print("Block not valid because previous block hash is not in the blockchain")
            write_log("Block not valid because previous block hash is not in the blockchain")
            return False
        # If the proof of work is invalid, False is returned
        if not self.is_valid_proof(block, block.generate_hash()):
            print("the proof of work is invalid, False is returned")
            write_log("the proof of work is invalid, False is returned")
            return False
        # Verify that the transaction is valid
        print(block.transactions)
        write_log(block.transactions)
        if not checkTransactions(block.transactions):
            print("the transaction is not valid")
            write_log("the transaction is not valid")
        nonceSet = set()
        # verify nouce is random
        for item in self.blockchain.values():
            if item.nonce not in nonceSet:
                nonceSet.add(item.nonce)
            else:
                print("nonce is not unique")
                write_log("nonce is not unique")
                return False
        if block.nonce in nonceSet:
            print("The newly added block nonce repeats the blockchain nonce")
            write_log("The newly added block nonce repeats the blockchain nonce")
            return False

        tmpChain = copy.deepcopy(self)
        tmpChain.blockchain[block.hash] = block
        if not tmpChain.is_valid_chain():
            return False

        parent_node = self.blockchain[prev_hash]
        height = parent_node.height + 1
        if (height <= self.maxheightnode.height - MAX_BRANCH_LEN_DIFF):
            print("Block not valid because of invalid forking")
            write_log("Block not valid because of invalid forking")
            return False
        if height > self.maxheightnode.height:
            self.maxheightnode = block
        self.blockchain[block.hash] = block
        print("new block with hash = {block.hash()} gets added in the block-chain")
        write_log("new block with hash = {block.hash()} gets added in the block-chain")
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Verify that the hash code in the block has several pre-zeros
        :param block: The block that needs to be verified
        :param block_hash: The hash of the block that needs to be verified
        :return:True or False
        """
        return (block_hash[:].startswith('0' * DIFFICULTY) and block.hash == block_hash)

    def getChainMessage(self):
        """
        show the blockchain info
        :return:
        """
        chainMessage = [i.getBlockMessage() for i in self.blockchain.values()]
        # print(chainMessage)
        return chainMessage

    def is_valid_chain(self):
        """
        Check if the blockchain is legal
        :return:True or False
        """
        prev_block_hash = self.genesis.hash
        for current_block_hash in self.blockchain:
            if self.blockchain[current_block_hash].height == 0:
                continue
            current_block = self.blockchain[current_block_hash]
            # print("****:",current_block.getBlockMessage())
            # print("*******",prev_block_hash)
            if current_block.previousHash != prev_block_hash:
                print("The hash of the current block is not the same as the hash of the previous block")
                write_log("The hash of the current block is not the same as the hash of the previous block")
                return False
            recomputed_current_hash = current_block.generate_hash()
            if not self.is_valid_proof(current_block, recomputed_current_hash):
                print("The hash of the current block does not meet the proof of work")
                write_log("The hash of the current block does not meet the proof of work")
                return False
            prev_block_hash = recomputed_current_hash
        return True

    def getMaxHeightBlock(self):
        """
        get the max height Block of block chain
        :return:
        """
        return self.maxheightnode


if __name__ == "__main__":
    bc = BlockChain()
    block = bc.genesis
    transaction1 = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
    transaction2 = Transaction(from_ip='192.168.42.11', to_ip='192.168.42.12', value=1.25)
    block2 = Block([transaction1, transaction2], block, block.hash)
    bc.add_block(block2, block2.hash)
    bc.getChainMessage()
    # print("�?前区块链�?否合法：", bc.is_valid_chain())
    # lastBlock=bc.getMaxHeightBlock()
    # print("lastBlock:",lastBlock.getBlockMessage())
    # 恶意篡改其中的hash
    # print("篡改前一�?区块的hash")
    # block2.previousHash="7508db73d954caaa2173f0bb0412263350c4faebece1845affbfe8f24fb34kjd"
    # print("�?前区块链�?否合法：",bc.is_valid_chain())
    # print("�?改工作量")
    mining_effort = 2
    print("�?前区块链�?否合法：", bc.is_valid_chain())

    print('\n\n\n')
    from Database import BlockChainDB

    db = BlockChainDB()
    bc = db.read()
    print(bc.getChainMessage())
