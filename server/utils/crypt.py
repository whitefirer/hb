#coding: utf8

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
class Crypt():
    def __init__(self, key):
        self.key = bytes(key, encoding="utf8")
        self.mode = AES.MODE_CBC
     
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        text = bytes(text, encoding="utf8")
        self.ciphertext = cryptor.encrypt(text)
        plain_text = b2a_hex(self.ciphertext)
        return str(plain_text, encoding="utf8")
     
    def decrypt(self, text):
        text = bytes(text, encoding="utf8")
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_text = str(plain_text, encoding="utf8")
        return plain_text.rstrip('\0')

if __name__ == '__main__':
    pc = Crypt('areyoukiddingme?')
    e = pc.encrypt("mod and addition")
    d = pc.decrypt(e)
    print(e, d)
    e = pc.encrypt("00000000000000000000000000")
    d = pc.decrypt(e)
    print(e, d)
    pc = Crypt('1546208823357502')
    #e = pc.encrypt('c357cf26d23813af3ea9592dc45394f82bbb8137d225a0dbb2a7e069a1765c2c')
    d = pc.decrypt("bcaff27742f454e9e7558ffe946120d7aaf199767958df57a97936b4008303e2")
    print(d)
    import base64
    print(base64.b64decode(d).decode('utf8'))
    answer = bytes('口令：苟利国家生死以岂因祸福避趋之', 'utf-8')
    answer = base64.b64encode(answer).decode('utf-8')
    e = pc.encrypt(answer)
    d = pc.decrypt(e)
    print(e, base64.b64decode(d).decode('utf8'))
    pc = Crypt('1546238330504274')
    print(a2b_hex("15f5c253742365d36bc101c8acbb5fa5"))
    d = pc.decrypt("15f5c253742365d36bc101c8acbb5fa5")
    print(d)