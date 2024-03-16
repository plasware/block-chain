from Database import AccountBookDB,Addr2PublicKeyDB


def checkTransactions(transactions):
        """
        check transactions signature and value
        Input:
            transactions: the transactions of block
        Output:
            bool represents check sucess or failure
        """
        # check value
        accountDB=AccountBookDB()
        accountInfo=accountDB.read()
        for transaction in transactions:
            publicDB=Addr2PublicKeyDB()
            publicKeyInfo=publicDB.read()
            public_key=publicKeyInfo[transaction.from_ip]
            if not transaction.check_signature(public_key):
                print("signature failure")
                return False
            if accountInfo[transaction.from_ip]<transaction.value:
                print("value failure")
                return False
            accountInfo[transaction.from_ip]-=transaction.value
        return True


def updateAccountBook(transactions):
    """
    update the account_book.json
    Input:
        transactions: the transactions of block
    Ouput:
    """
    for transaction in transactions:
        accountDB=AccountBookDB()
        accountInfo=accountDB.read()
        accountInfo[transaction.from_ip]-=transaction.value
        accountInfo[transaction.to_ip]+=transaction.value
        
    accountDB.write(accountInfo)
    print("update accountbook success")
     