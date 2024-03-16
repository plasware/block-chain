from Constant import *
from os.path import join as pjoin
import json
import pickle

class BaseDB():
    filepath = DATA_PATH

    def __init__(self, filename):
        self.filepath = pjoin(self.filepath, filename)

    def read(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def write(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f)

class TransactionDB(BaseDB):
    def __init__(self):
        super().__init__('transactions.pkl')

    def read(self):
        with open(self.filepath, 'rb') as f:
            return pickle.load(f)
    
    def write(self, transaction):
        '''
        Input:
            transaction: a Transaction object
        '''
        with open(self.filepath, 'wb') as f:
            pickle.dump(transaction, f)
        
    def append(self, transaction):
        '''
        Input:
            transaction: a Transaction object
        Output:
            the length of the transaction list
        '''
        transactions = self.read()
        transactions.append(transaction)
        self.write(transactions)
    
class BlockChainDB(BaseDB):
    def __init__(self):
        super().__init__('blockchain.pkl')

    def read(self):
        with open(self.filepath, 'rb') as f:
            return pickle.load(f)
    
    def write(self, blockchain):
        '''
        Input:
            transaction: a Transaction object
        '''
        with open(self.filepath, 'wb') as f:
            pickle.dump(blockchain, f)

class AccountBookDB(BaseDB):
    def __init__(self):
        super().__init__('account_book.json')

class Addr2PublicKeyDB(BaseDB):
    '''
    format: {addr(str): public_key(str)}
    '''
    def __init__(self):
        super().__init__('addr2public_key.json')
