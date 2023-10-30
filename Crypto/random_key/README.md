# Crypto / Random_key

## Challenge
An encrypted message sent by ALICE to its control center has been intercepted.

You have managed to get your hands on some code snippets used by ALICE to encrypt its message, as well as the ciphertext. Your mission is to recover the message in clear text.

> Enc: 21952f9ced6c9109f8ce7c41cd3e0e6981c97a84745d5fdc75b2584e9a5a05e0

## Inputs
- challenge: [challenge.py](./challenge.py)
- key generation: [generate_key.c](./generate_key.c)

## Solution
We first build the provided c code as a shared library after adding the missing dependancies:
```c
#include <openssl/md5.h>
#include <time.h>
#include <stdio.h>
#include <string.h>

unsigned char key[32] = { 0 };
(...)
```

```console
$ gcc generate_key.c -fPIC -shared -lcrypto -o generate_key.so
```

Shared library `generate_key.so` is generated in current directory.

Then we can run the provided python code, where a print statement is added to dump the generated key (and we also add some fake flag):

```console
$ python3 challenge.py
Un message chiffré a été envoyé par l'IA ALICE à son centre de contrôle. Vous avez réussi à mettre la main sur certains extraits de code utilisés par ALICE pour chiffrer son message ainsi que sur le texte chiffré. Votre mission est de retrouver le message en clair.
key b'134abb7bd9d248a9'
Enc: 26fbe4526b6a07a76212e34b516d6a5f
```

Now, the point is that this key is absolutely NOT random ! Let's look at how it is generated:

```c
unsigned char *generate_256bits_encryption_key(unsigned char *recipient_name)
{
	int i = 0;
	FILE *f = NULL;
	time_t now1 = 0L;
	time_t now2 = 0L;
	time_t delta = 0L;
	
	now1 = time(NULL);
	
	f = fopen("/dev/urandom", "rb");
	fread(&key, 1, 32, f);
	fclose(f);
	
	md5(recipient_name, key);
	
	now2 = time(NULL);
	delta = now2 - now1;
	
	key[8] = delta;
	
	return key;
}
```

```python
	key = generate_256bits_encryption_key(b'Control_center').hex().encode()
```

In `generate_256bits_encryption_key()`, we read 32 bytes from `/dev/urandom`, write it to `key`, then `md5` input b'Control_center' and... write it to key. So instead of generating a 32 bytes key, we generate a fixed 16 bytes key !

So we have (iv, key), let's decrypt the encoded message:

```python
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

key = b'134abb7bd9d248a9'
iv  = b'FEDCBA9876543210'
c   = long_to_bytes(0x21952f9ced6c9109f8ce7c41cd3e0e6981c97a84745d5fdc75b2584e9a5a05e0)
print(AES.new(key, AES.MODE_CBC, iv).decrypt(c).decode())
```

```console
$ python3 sol.py
ECW{random_key_7AgmwlBXo1tDhyqR}

```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
ECW{random_key_7AgmwlBXo1tDhyqR}
