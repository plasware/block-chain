from Transaction import Transaction

from Block import Block

# Mining difficulty factor
mining_effort=0
# 最大分支长度
max_branch_len_diff = 10


class BlockChain:
    def __init__(self):
        """
        init a block chain
        """
        self.blockchain = dict({})
        genesis_block=self.genesisBlock()
        self.maxheightnode=genesis_block
        self.genesis =genesis_block
        self.blockchain[genesis_block.hash]=genesis_block
        self.transactions=[]

    # 祖先区块
    def genesisBlock(self):
        """
        create a genesis block
        :return: a genesis block
        """
        block=Block(genesis_block=True)
        return block

    def add_block(self, block=None, proof=None):
        """
        add a block to block chain
        :param block: the block need to add
        :param proof: the hash of block
        :return: True or False
        """
        prev_hash = block.previousHash
        print(prev_hash)
        # If the hash value of the previous block is empty, False is returned
        if prev_hash == None:
            print("Block not valid because previous block hash is None")
            return False
        # If the hash of the previous block is not in the blockchain, False is returned
        if prev_hash not in self.blockchain:
            print("Block not valid because previous block hash is not in the blockchain")
            return False
        # If the proof of work is invalid, False is returned
        if not self.is_valid_proof(block, proof):
            print("the proof of work is invalid, False is returned")
            return False
        #Verify that the transaction is valid
        # totalTransactions=block.transactions
        # for transaction in totalTransactions:
        #     #not valid
        #     if not transaction.check_signature():
        #         print("transaction not valid")
        #         return False

        parent_node = self.blockchain[prev_hash]
        height = parent_node.height + 1
        if (height <= self.maxheightnode.height - max_branch_len_diff):
            print("Block not valid because of invalid forking")
            return False
        if height > self.maxheightnode.height:
            self.maxheightnode = block
        self.blockchain[block.hash] = block
        print("new block with hash = {block.get_hash()} gets added in the block-chain")
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Verify that the hash code in the block has several pre-zeros
        :param block: The block that needs to be verified
        :param block_hash: The hash of the block that needs to be verified
        :return:True or False
        """
        return (block_hash[:].startswith('0' * mining_effort) and block.hash == block_hash)


    def getChainMessage(self):
        """
        show the blockchain info
        :return:
        """
        chainMessage = [i.getBlockMessage() for i in self.blockchain.values()]
        print(chainMessage)
        # return chainMessage

    def is_valid_chain(self):
        """
        Check if the blockchain is legal
        :return:True or False
        """
        prev_block_hash = hex(0)
        for current_block_hash in self.blockchain:
            current_block = self.blockchain[current_block_hash]
            if current_block.previousHash != prev_block_hash:
                print("The hash of the current block is not the same as the hash of the previous block")
                return False
            recomputed_current_hash = current_block.generate_hash()
            if not self.is_valid_proof(current_block, recomputed_current_hash):
                print("The hash of the current block does not meet the proof of work")
                return False
            prev_block_hash = recomputed_current_hash
        return True

    def getMaxHeightBlock(self):
        """
        get the max height Block of block chain
        :return:
        """
        return self.maxheightnode


if __name__=="__main__":
    bc=BlockChain()
    block=bc.genesis
    transaction1 = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
    transaction2 = Transaction(from_ip='192.168.42.11', to_ip='192.168.42.12', value=1.25)
    block2=Block([transaction1,transaction2],block,block.hash)
    bc.add_block(block2,block2.hash)
    bc.getChainMessage()
    print("目前区块链是否合法：", bc.is_valid_chain())
    lastBlock=bc.getMaxHeightBlock()
    print("lastBlock:",lastBlock.getBlockMessage())
    #恶意篡改其中的hash
    # print("篡改前一个区块的hash")
    # block2.previousHash="7508db73d954caaa2173f0bb0412263350c4faebece1845affbfe8f24fb34kjd"
    # print("目前区块链是否合法：",bc.is_valid_chain())
    print("修改工作量")
    mining_effort = 2
    print("目前区块链是否合法：", bc.is_valid_chain())




