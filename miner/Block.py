import time
from Transaction import Transaction
import hashlib

initPreviousHash=hex(0)
class Block:
    def __init__(self, transactions=None, parent=None,previousHash='',genesis_block = False):
        """
        Initialize a Block
        param transactions: The block contains transactions
        param previousHash: Hash of the previous block
        param height: the height of Block
        """
        if genesis_block:
            # Genesis block initial transaction information
            self.transactions = [Transaction('创世','创世',0)]
            # The hash of the previous block is initialized to hex(0)
            self.previousHash = initPreviousHash
            #Block height
            self.height = 0
        else:
            # Block all transaction information
            self.transactions = transactions
            self.previousHash = previousHash
            self.height = self.getHeight(parent)
        self.parent = parent
        self.children = []
        self.timestamp = time.time()
        self.nonce=0
        self.hash=self.generate_hash()
        if self.parent is not None:
            self.parent.children.append(self)


    def getHeight(self,parent):
        """
        Get the current block height
        :param parent:Parent node of the current block
        :return: the current block height
        """
        return parent.height+1

    def generate_hash(self):
        """
        Generates a hash of the current block
        :return: A hash of the current block
        """
        data = str(self.transactions) + self.previousHash + str(self.timestamp) + str(self.nonce)
        return str(hashlib.sha256(data.encode('utf-8')).hexdigest())

    def getBlockMessage(self):
        """
        Get block information
        :return: None
        """
        transactionMessage = [i.getTransactionMessage() for i in self.transactions]
        blockMessage = {'transactions': transactionMessage,
                        'previousHash': self.previousHash,
                        'timestamp': self.timestamp,
                        'nonce': self.nonce,
                        'hash': self.hash,
                        "height":self.height,
                        "parent":self.parent,
                        "children":self.children
                        }
        return blockMessage

if __name__=="__main__":
    #Initializes a genesis block
    block=Block(genesis_block=True)
    #Initializes a new block,the parent block is genesis block
    #Initializes the transactions
    transaction1 = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
    transaction2 = Transaction(from_ip='192.168.42.11', to_ip='192.168.42.12', value=1.25)
    #Initializes the new block
    block2=Block([transaction1,transaction2],block,block.hash)
    # show the block information
    print(block2.getBlockMessage())
    print(block.getBlockMessage())