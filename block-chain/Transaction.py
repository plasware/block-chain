import time
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from write_log import write_log


class Transaction:
    def __init__(self, from_ip, to_ip, value, signature=None, time_stamp=None):
        """
        Initialize a transaction
        Input:
            from_ip: A str represents the ip of the one who gives the value out
            to_ip: A str represents the ip of the one who receives the ip
            value: A float represents the amount of value
        """
        self.time_stamp = time.time() if time_stamp is None else time_stamp  # time.time() return a float representing seconds since 1970.1.1
        self.from_ip = from_ip
        self.to_ip = to_ip
        self.value = value
        self.signature = signature

    def sign_signature(self, private_key):
        """
        Generate signature for current Transaction
        Input:
            private_key: a str representing private_key of current client
        Output:
            signature: a str of readable signature
        """
        sha256_result = self.generate_hash()
        _private_key = RSA.importKey(private_key)
        signer = pkcs1_15.new(_private_key)
        signature = signer.sign(sha256_result)

        # The result of signature is unreadable
        signature_str = base64.b64encode(signature).decode('utf-8')

        return signature_str

    def check_signature(self, public_key):
        """
        Check validity of the content
        Input:
            public_key: a str representing public_key of current client
        Output:
            A bool value of checking result
        """
        sha256_result = self.generate_hash()
        signature = base64.b64decode(self.signature)
        _public_key = RSA.importKey(public_key)
        verifier = pkcs1_15.new(_public_key)
        # official document at https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        try:
            verifier.verify(sha256_result, signature)
            return True
        except (ValueError, TypeError):
            return False

    def generate_hash(self):
        """
        Generate SHA256 hash value for current Transaction
        Input:
        Output:
            result: the hash result
        """
        str_to_hash = "time_stamp: {}, from: {}, to: {}, value: {}".format(
            str(self.time_stamp), self.from_ip, self.to_ip, str(self.value))
        result = SHA256.new(str_to_hash.encode('utf-8'))

        return result

    def check_value(self, from_value):
        """
        Check whether from account has enough value for current transaction
        Input:
            from_value: A float of from account value
        Output:
            A bool value of checking result
        """
        if from_value >= self.value:
            return True
        else:
            return False
        
    def __str__(self):
        return "fromIp:{},toIp:{},value:{},sig:{}".format(self.from_ip,self.to_ip,self.value,self.signature)

    def to_dict(self):
        """
        Convert the Transaction to a dictionary
        """
        return {
            'time_stamp': self.time_stamp,
            'from_ip': self.from_ip,
            'to_ip': self.to_ip,
            'value': self.value,
            'signature': self.signature
        }
    
    def from_dict(self, data):
        """
        Load the Transaction from a dictionary
        """
        self.time_stamp = data['time_stamp']
        self.from_ip = data['from_ip']
        self.to_ip = data['to_ip']
        self.value = data['value']
        self.signature = data['signature']


if __name__ == '__main__':
    # Test
    transaction = Transaction(from_ip='192.168.42.10', to_ip='192.168.42.11', value=1.23)
    print('transaction:\n', str(transaction))

    
    print(transaction.check_value(1.11))
    print(transaction.check_value(2.34))
    rsa = RSA.generate(2048)
    private_key = rsa.exportKey().decode('utf-8')
    public_key = rsa.publickey().exportKey().decode('utf-8')
    print(private_key)
    print(public_key)
    transaction.signature = transaction.sign_signature(private_key)
    print(transaction.signature)
    print(transaction.check_signature(public_key))

    from Database import TransactionDB
    db = TransactionDB()
    db.write([])
    print(db.read())

