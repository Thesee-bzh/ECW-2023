from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

key = b'134abb7bd9d248a9'
iv  = b'FEDCBA9876543210'
c   = long_to_bytes(0x21952f9ced6c9109f8ce7c41cd3e0e6981c97a84745d5fdc75b2584e9a5a05e0)
print(AES.new(key, AES.MODE_CBC, iv).decrypt(c).decode())

# ECW{random_key_7AgmwlBXo1tDhyqR}
