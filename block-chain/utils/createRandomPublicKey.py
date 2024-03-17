import json
import random
import string
from Crypto.PublicKey import RSA

def generate_public_key(i):
    rsa = RSA.generate(i+1024)
    private_key = rsa.exportKey().decode('utf-8')
    public_key = rsa.publickey().exportKey().decode('utf-8')
    return private_key,public_key


publicKey_data = {}
privateKey_data= {}

for i in range(100):
    addr="192.168.42." + str(i)
    public_key,private_key = generate_public_key(i)
    publicKey_data[addr] = public_key
    privateKey_data[addr]=private_key


with open('addr2public_key.json', 'w') as file:
    json.dump(publicKey_data, file, indent=4)

with open('addr2private_key.json', 'w') as file:
    json.dump(privateKey_data, file, indent=4)

print("finish")
