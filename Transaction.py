import time


class Transaction:
    def __init__(self, from_ip, to_ip, value):
        """
        Initialize a transaction
        Input:
            from_ip: A str represents the ip of the one who gives the value out
            to_ip: A str represents the ip of the one who receives the ip
            value: A float represents the amount of value
        """
        self.time_stamp = time.time()
        self.from_ip = from_ip
        self.to_ip = to_ip
        self.value = value

    def sign(self):
        # TODO: generate signature
        pass

    # TODO: check the transaction is legal
