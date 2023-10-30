# Misc / jigsaw2

## Challenge
To get the flags, you will have to answer to all questions in a limited time. Don't forget to check the leaderboard.

## Inputs
- Docker instance

## Solution
We're asked a couple of questions. We use `pwntools` to script the interaction with the docker instance. Since the questions are of different nature, we build the script one question after the other.

Every single question is handled in a separate function (take away from `jigsaw1` last year).

First questions are trivial.

### Question 3
"Easy question, Which letter comes after : h". Can be `after` or `before`. Of course the letter may not be the same. Implementation:
```python
    if b"before" in req:
        op = -1
    else:
        op = +1
    print(req.decode())
    resp = chr(req[-1]+op).encode()
```

### Question 4
"Can you tell me what color is : 255,0,0". So we get `RGB` values and need to identify the name of the color. I used `rgb_to_name()` from module `webcolors`. Only thing is, it gives me `lime` instead of `green` for `0,255,0`, so I need to patch this one. Implementation:
```python
    rgb = req.decode().split(',')
    l = [int(rgb[0]), int(rgb[1]), int(rgb[2])]
    color = tuple(l)
    resp = rgb_to_name(color).encode()
    if resp == b'lime':
        resp = b'green'
```

### Flag1
After that we get the first flag:
> Congratulations for the first steps. Your first flag is : ECW{J1GS4W_R3TURNS}

### Question 5
"I forgot everything. Send me back your answers to questions 1 to 4, separated by commas". So we simply need to store the consecutive responses in a list. Implementation:
```python
    resp = resp_l[0] + b',' + resp_l[1] + b',' + resp_l[2] + b',' + resp_l[3]
```

### Question 6
"I did not understand. Can you repeat your previous answers for question(s) 2 using the same format ?". Of course the list of questions may vary. Implementation:
```python
    req = req.decode().split(" using")[0].split(',')
    req_l = [int(x) for x in req]
    resp = b''
    for i in range(len(req_l)):
        resp += resp_l[req_l[i] - 1]
        if (i != len(req_l) - 1):
            resp += b','
```

### Question 7
"Just to be sure it wasn't luck, random question time : What is the meaning of life, the universe, and everything, according to Deep Thought?". Ok, random question now. Handling every single question in a separate function makes it easier. Implementation:
```python
Q1 = b"1. Do you wanna play a game?"
Q2 = b"2. What is the meaning of life, the universe, and everything, according to Deep Thought?"
Q3 = b"3. Easy question, Which letter comes "
# (...)

def q7():
    # (...)
    # Identify the random question
    # Starting number is not provided, so match with the question itself (Q1, Q2, etc.)
    # Skip the starting number when matching Q1, Q2, etc. since it is not provided...
    if Q1[3:].lower() in req:
        print("Q1")
        q1(random=True)
    elif Q2[3:].lower() in req:
        print("Q2")
        q2(random=True)
    elif Q3[3:].lower() in req:
        print("Q3")
        q3(random=True, req=req)
    elif Q4[3:].lower() in req:
        print("Q4")
        q4(random=True, req=req)
    elif Q5[3:].lower() in req:
        print("Q5")
        q5(random=True)
    elif Q6[3:].lower() in req:
        print("Q6")
        q6(random=True, req=req)
```

### Flag2
Now we get the second flag:
> Well done ! Here is your flag : ECW{N0T_SC3R3D_Y3T}

### Question 8
Some `Morse` of `Braille` code like this for instance:
```
8.
⠎ ⠑ ⠝ ⠙ ⠀ ⠍ ⠑ ⠀ ⠃ ⠁ ⠉ ⠅ ⠀ ⠞ ⠓ ⠑ ⠀ ⠋ ⠕ ⠇ ⠇ ⠕ ⠺ ⠊ ⠝ ⠛ ⠀ ⠺ ⠕ ⠗ ⠙ ⠀ : ⠀ ⠝ ⠑ ⠥ ⠗ ⠁ ⠇ ⠀ ⠝ ⠑ ⠞ ⠺ ⠕ ⠗ ⠅
```

Decoding this example: `send me back the following word : neural network`. Of course, the word to send back may vary...

Implementation:
```python
MORSE_CODE = {
        'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',   ':': '---...',
        ',': '--..--',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
}

MORSE_CODE_REVERSED = {value:key for key,value in MORSE_CODE.items()}


# ASCII
asciicodes = [' ','!','"','#','$','%','&','','(',')','*','+',',','-','.','/',
          '0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@',
          'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
          'r','s','t','u','v','w','x','y','z','[','\\',']','^','_',':',',']

# Braille symbols
brailles = ['⠀','⠮','⠐','⠼','⠫','⠩','⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌','⠴','⠂','⠆','⠒','⠲','⠢',
        '⠖','⠶','⠦','⠔','⠱','⠰','⠣','⠿','⠜','⠹','⠈','⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚','⠅',
        '⠇','⠍','⠝','⠕','⠏','⠟','⠗','⠎','⠞','⠥','⠧','⠺','⠭','⠽','⠵','⠪','⠳','⠻','⠘','⠸',':',',']

def from_morse(m):
    pt = ''
    for w in m.split('/'):
        pt += ''.join(MORSE_CODE_REVERSED.get(i) for i in w.split())
        pt += ' '
    return pt[:-1]

def from_braille(m):
    s = m.replace(' ', '')
    return ''.join([asciicodes[brailles.index(x)] for x in s])

def q8():
    # Q8 = b"8. " # Then some Morse/Braille code...
    try:
        c.recvuntil(Q8); print(Q8.decode())
    except:
        return False
    req = c.recvline().strip().decode()
    print(req)
    # Check for Morse/Braille code
    if (req[0] == '.' or req[0] == '-'):
        dec = from_morse(req)
    else:
        dec = from_braille(req)
    print(dec)
    q = "send me back the following word : "
    if not q in dec.lower():
        assert()
    resp = dec.lower().split(q)[1].encode()
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True
```

### Question 9
A PNG image to decode. This image contains a `QR code`:
```
[DEBUG] Received 0x24c bytes:
    00000000  39 2e 20 89  50 4e 47 0d  0a 1a 0a 00  00 00 0d 49  │9. ·│PNG·│····│···I│
    00000010  48 44 52 00  00 01 9a 00  00 01 9a 01  00 00 00 00  │HDR·│····│····│····│
    00000020  1e 7d b8 ce  00 00 02 10  49 44 41 54  78 9c ed 9a  │·}··│····│IDAT│x···│
(...)
```

For this one, I'm using `img = Image.open(io.BytesIO(data))` to grab the data and make it an image thanks to library `PIL`, then `read_barcodes(img)` from `zxingcpp` to decode the `QR code` and recover the plaintext. The plaintext itself is like "Send me back the following word : regression", where the word to send back may vary. Oh come on, this is becoming ridiculous... Implementation:

```python
def q9():
    # Q9 = b"9. " # Then a PNG image with plaintext
    print("Enter Q9")
    try:
        c.recvuntil(Q9); print(Q9.decode())
    except:
        return False
    data = c.recvuntil(b'IEND\xaeB\x60\x82')
    img = Image.open(io.BytesIO(data))
    results = zxingcpp.read_barcodes(img)
    dec = results[0].text
    print(dec)
    # We decoded a paintext question...
    q = "Send me back the following word : "
    if q not in dec:
        assert()
    resp = dec.split(q)[1].encode()
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True
```

### Question 10
Again a PNG image containing a `QR code`. But this time, the `QR code` decodes into `Morse` or `Braille`, which then asks to answer a random question. So PNG -> QR -> Morse/Braille -> random question. For instance:
```
10.
.- -. ... .-- . .-. / - .... . / ..-. --- .-.. .-.. --- .-- .. -. --. / --.- ..- . ... - .. --- -. / ---... / -.-. .- -. / -.-- --- ..- / - . .-.. .-.. / -- . / .-- .... .- - / -.-. --- .-.. --- .-. / .. ... / ---... / ----- --..-- ----- --..-- ..--- ..... .....
ANSWER THE FOLLOWING QUESTION : CAN YOU TELL ME WHAT COLOR IS : 0,0,255
```

Implementation:
```python
def q10():
    # Q10 = b"10. " # Then a PNG image with Morse/Braille code
    print("Enter Q10")
    try:
        c.recvuntil(Q10); print(Q10.decode())
    except:
        return False
    data = c.recvuntil(b'IEND\xaeB\x60\x82')
    img = Image.open(io.BytesIO(data))
    results = zxingcpp.read_barcodes(img)
    dec = results[0].text.strip()
    print(dec)
    # Check for Morse/Braille code
    if (dec[0] == '.' or dec[0] == '-'):
        m = from_morse(dec)
    else:
        m = from_braille(dec)
    print(m)
    q = "answer the following question : "
    if q not in m.lower():
        assert()
    req = m.lower().split(q)[1].lower().encode()
    return q7(skip=True, req=req)
```

### Flag3
After that, we get our Third flag:
> You've done it ! The last flag is : ECW{R4ND0M_ST3G4N0}

I didn't go any further (there was a last piece of that nightmare to solve).

### Interaction stream output
Here is the output of one interaction with the docker instance, with `pwntools DEBUG` mode enabled:

```console
$ python3 sol.py DEBUG
[+] Opening connection to instances.challenge-ecw.fr on port 38082: Done
[DEBUG] Received 0x5c bytes:
    b"Welcome ! If you want to leave alive, you'll have to answer correctly to all my questions !\n"
[DEBUG] Received 0x1d bytes:
    b'1. Do you wanna play a game?\n'
1. Do you wanna play a game?
[DEBUG] Sent 0x4 bytes:
    b'yes\n'
yes
[DEBUG] Received 0x59 bytes:
    b'2. What is the meaning of life, the universe, and everything, according to Deep Thought?\n'
2. What is the meaning of life, the universe, and everything, according to Deep Thought?
[DEBUG] Sent 0x3 bytes:
    b'42\n'
42
[DEBUG] Received 0x2f bytes:
    b'3. Easy question, Which letter comes after : h\n'
3. Easy question, Which letter comes
after : h
[DEBUG] Sent 0x2 bytes:
    b'i\n'
i
[DEBUG] Received 0x2b bytes:
    b'4. Can you tell me what color is : 255,0,0\n'
4. Can you tell me what color is :
255,0,0
[DEBUG] Sent 0x4 bytes:
    b'red\n'
red
[DEBUG] Received 0x4e bytes:
    b'Congratulations for the first steps. Your first flag is : ECW{J1GS4W_R3TURNS}\n'
[DEBUG] Received 0x5c bytes:
    b'5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.\n'
5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.
[DEBUG] Sent 0xd bytes:
    b'yes,42,i,red\n'
yes,42,i,red
[DEBUG] Received 0x68 bytes:
    b'6. I did not understand. Can you repeat your previous answers for question(s) 2 using the same format ?\n'
6. I did not understand. Can you repeat your previous answers for question(s)
['2']
[DEBUG] Sent 0x3 bytes:
    b'42\n'
42
[DEBUG] Received 0x90 bytes:
    b"7. Just to be sure it wasn't luck, random question time : What is the meaning of life, the universe, and everything, according to Deep Thought?\n"
7. Just to be sure it wasn't luck, random question time :
what is the meaning of life, the universe, and everything, according to deep thought?
Q2
[DEBUG] Sent 0x3 bytes:
    b'42\n'
42
[DEBUG] Received 0x35 bytes:
    b'Well done ! Here is your flag : ECW{N0T_SC3R3D_Y3T} \n'
[DEBUG] Received 0xc1 bytes:
    00000000  38 2e 20 e2  a0 8e 20 e2  a0 91 20 e2  a0 9d 20 e2  │8. ·│·· ·│·· ·│·· ·│
    00000010  a0 99 20 e2  a0 80 20 e2  a0 8d 20 e2  a0 91 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000020  a0 80 20 e2  a0 83 20 e2  a0 81 20 e2  a0 89 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000030  a0 85 20 e2  a0 80 20 e2  a0 9e 20 e2  a0 93 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000040  a0 91 20 e2  a0 80 20 e2  a0 8b 20 e2  a0 95 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000050  a0 87 20 e2  a0 87 20 e2  a0 95 20 e2  a0 ba 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000060  a0 8a 20 e2  a0 9d 20 e2  a0 9b 20 e2  a0 80 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000070  a0 ba 20 e2  a0 95 20 e2  a0 97 20 e2  a0 99 20 e2  │·· ·│·· ·│·· ·│·· ·│
    00000080  a0 80 20 3a  20 e2 a0 80  20 e2 a0 9d  20 e2 a0 91  │·· :│ ···│ ···│ ···│
    00000090  20 e2 a0 a5  20 e2 a0 97  20 e2 a0 81  20 e2 a0 87  │ ···│ ···│ ···│ ···│
    000000a0  20 e2 a0 80  20 e2 a0 9d  20 e2 a0 91  20 e2 a0 9e  │ ···│ ···│ ···│ ···│
    000000b0  20 e2 a0 ba  20 e2 a0 95  20 e2 a0 97  20 e2 a0 85  │ ···│ ···│ ···│ ···│
    000000c0  0a                                                  │·│
    000000c1
8.
⠎ ⠑ ⠝ ⠙ ⠀ ⠍ ⠑ ⠀ ⠃ ⠁ ⠉ ⠅ ⠀ ⠞ ⠓ ⠑ ⠀ ⠋ ⠕ ⠇ ⠇ ⠕ ⠺ ⠊ ⠝ ⠛ ⠀ ⠺ ⠕ ⠗ ⠙ ⠀ : ⠀ ⠝ ⠑ ⠥ ⠗ ⠁ ⠇ ⠀ ⠝ ⠑ ⠞ ⠺ ⠕ ⠗ ⠅
send me back the following word : neural network
[DEBUG] Sent 0xf bytes:
    b'neural network\n'
neural network
Enter Q9
[DEBUG] Received 0x24c bytes:
    00000000  39 2e 20 89  50 4e 47 0d  0a 1a 0a 00  00 00 0d 49  │9. ·│PNG·│····│···I│
    00000010  48 44 52 00  00 01 9a 00  00 01 9a 01  00 00 00 00  │HDR·│····│····│····│
    00000020  1e 7d b8 ce  00 00 02 10  49 44 41 54  78 9c ed 9a  │·}··│····│IDAT│x···│
    00000030  4b 8e 84 30  0c 44 2d f5  01 38 12 57  9f 23 71 00  │K··0│·D-·│·8·W│·#q·│
    00000040  a4 34 b1 cb  76 42 33 33  ea 6d 5c 5e  84 00 7e ac  │·4··│vB33│·m\^│··~·│
    00000050  4a fe 05 69  df db 8f 10  22 44 88 10  21 42 84 08  │J··i│····│"D··│!B··│
    00000060  39 24 b0 d7  f5 64 eb b7  db 29 d7 3b  b9 96 be 6b  │9$··│·d··│·)·;│···k│
    00000070  87 3b ec 84  8a 40 7a d3  8e 57 df 9d  d7 bb ee d5  │·;··│·@z·│·W··│····│
    00000080  17 f5 d7 17  83 1f a1 0a  90 79 a9 8c  42 41 aa 2a  │····│····│·y··│BA·*│
    00000090  e9 1f ea 5f  13 dd 11 2a  07 a9 64 d4  55 6c 81 8c  │···_│···*│··d·│Ul··│
    000000a0  08 15 85 f0  6e de fd 27  23 42 0b 42  7a f1 c0 32  │····│n··'│#B·B│z··2│
    000000b0  e4 9b 90 d1  e0 47 a8 00  04 9b 74 33  2e ee 40 a8  │····│·G··│··t3│.·@·│
    000000c0  08 74 b3 a9  41 09 91 85  11 5a 1f 4a  c9 58 60 11  │·t··│A···│·Z·J│·X`·│
    000000d0  eb 5b 81 2b  a4 c1 86 50  15 28 5d 7d  88 d1 bc 1c  │·[·+│···P│·(]}│····│
    000000e0  d5 67 5d 50  ad 9d b7 c0  42 68 61 a8  45 6f d2 a6  │·g]P│····│Bha·│Eo··│
    000000f0  56 05 d2 ca  44 44 a8 06  e4 a1 23 04  e5 dd aa ee  │V···│DD··│··#·│····│
    00000100  dc 6e 32 22  b4 36 84 8e  04 41 24 8a  50 54 a2 49  │·n2"│·6··│·A$·│PT·I│
    00000110  12 2a 01 61  70 b5 61 37  9e 7e cc 55  c9 4e a8 08  │·*·a│p·a7│·~·U│·N··│
    00000120  64 7d 48 a4  15 13 8f 7a  dd 72 10 a1  1a 90 39 44  │d}H·│···z│·r··│··9D│
    00000130  39 8a 9a d4  cb 51 eb 60  d5 8f 50 11  48 35 32 55  │9···│·Q·`│··P·│H52U│
    00000140  9d a7 78 d3  82 5a 64 18  67 10 5a 1f  32 b5 ec b9  │··x·│·Zd·│g·Z·│2···│
    00000150  3b 5e 43 89  6a 50 f3 67  84 aa 40 5e  81 8c 63 2d  │;^C·│jP·g│··@^│··c-│
    00000160  8b 33 91 65  08 d5 81 44  a6 64 32 e7  16 28 e8 3e  │·3·e│···D│·d2·│·(·>│
    00000170  1d 25 b4 2e  74 5d bd 0f  d1 a4 03 3b  7f f9 24 a1  │·%·.│t]··│···;│··$·│
    00000180  f5 21 3c 39  fd 6f cc e6  cb d0 b9 6c  ee 48 68 7d  │·!<9│·o··│···l│·Hh}│
    00000190  c8 a7 57 5d  2d d3 e8 1b  66 d2 fa 18  74 12 5a 16  │··W]│-···│f···│t·Z·│
    000001a0  d2 c0 62 0a  42 1f 92 7f  68 0a 7e d3  8c 38 43 a8  │··b·│B···│h·~·│·8C·│
    000001b0  00 84 ca 22  ca d1 ae 16  d4 a4 61 0f  e7 ee 84 96  │···"│····│··a·│····│
    000001c0  85 d2 d0 aa  e8 3b 9f 68  79 6f f2 31  2f 27 b4 2c  │····│·;·h│yo·1│/'·,│
    000001d0  e4 52 99 e2  87 b5 25 9e  79 72 b0 41  a8 02 b4 bb  │·R··│··%·│yr·A│····│
    000001e0  57 de 0a ce  d1 7d c0 15  f3 6f 42 25  a0 49 2d d9  │W···│·}··│·oB%│·I-·│
    000001f0  c1 da 12 a9  e6 a1 86 25  b4 38 94 2d  ab 37 2d 08  │····│···%│·8·-│·7-·│
    00000200  36 84 8a 42  79 42 2a 71  84 6e fe 11  62 08 95 80  │6··B│yB*q│·n··│b···│
    00000210  f4 72 60 d0  f9 84 b7 a7  96 95 d0 b2  10 cc d3 4a  │·r`·│····│····│···J│
    00000220  ca 28 4f cb  fe 68 50 08  2d 07 7d 67  84 08 11 22  │·(O·│·hP·│-·}g│···"│
    00000230  44 88 10 21  42 1d 7a 03  73 83 a6 6f  c1 86 d9 c7  │D··!│B·z·│s··o│····│
    00000240  00 00 00 00  49 45 4e 44  ae 42 60 82               │····│IEND│·B`·│
    0000024c
9.
Send me back the following word : regression
[DEBUG] Sent 0xb bytes:
    b'regression\n'
regression
Enter Q10
[DEBUG] Received 0x586 bytes:
    00000000  31 30 2e 20  89 50 4e 47  0d 0a 1a 0a  00 00 00 0d  │10. │·PNG│····│····│
    00000010  49 48 44 52  00 00 02 8a  00 00 02 8a  01 00 00 00  │IHDR│····│····│····│
    00000020  00 92 0f 47  21 00 00 05  49 49 44 41  54 78 9c ed  │···G│!···│IIDA│Tx··│
    00000030  9a c1 8d eb  30 0c 44 09  b8 00 97 a4  d6 5d 92 0b  │····│0·D·│····│·]··│
    00000040  30 a0 1f 8b  33 24 ed ec  e5 03 7b 58  80 a3 83 12  │0···│3$··│··{X│····│
    00000050  cb e2 53 2e  03 92 a3 d8  fc ed 71 98  90 42 0a 29  │··S.│····│··q·│·B·)│
    00000060  a4 90 42 0a  29 a4 90 42  0a 29 e4 df  43 1a c6 76  │··B·│)··B│·)··│C··v│
    00000070  af dc d3 3e  fd db 5a 9d  f3 fc 4c f7  9a 8d 79 f9  │···>│··Z·│··L·│··y·│
    00000080  63 79 11 8f  9f b7 42 0a  d9 0f b9 1e  e6 b9 79 d0  │cy··│··B·│····│··y·│
    00000090  82 fb 34 3e  6b fe c2 76  1e 0d ee 5a  c3 b7 42 11  │··4>│k··v│···Z│··B·│
    000000a0  52 c8 6e c8  5b 54 2b fc  b0 25 be 2b  64 78 7f bb  │R·n·│[T+·│·%·+│dx··│
    000000b0  19 4b 9f 1e  f4 59 5b 11  14 64 9c 2f  a4 90 ad 91  │·K··│·Y[·│·d·/│····│
    000000c0  19 ee 0a dc  5f 72 0d 55  e6 81 42 0a  29 e4 78 a4  │····│_r·U│··B·│)·x·│
    000000d0  b3 52 0c 1e  4e d9 5c 8b  55 90 53 48  21 85 a4 e4  │·R··│N·\·│U·SH│!···│
    000000e0  bc 95 9a 27  25 e7 32 8c  8a 70 b0 04  f4 1f 61 86  │···'│%·2·│·p··│··a·│
    000000f0  17 85 22 a4  90 cd 90 46  c9 41 95 ff  37 31 5c 48  │··"·│···F│·A··│71\H│
    00000100  21 1b 22 cb  38 fc 1d b2  16 1a 28 0a  12 99 6c 89  │!·"·│8···│··(·│··l·│
    00000110  2f d5 fb 06  08 29 64 27  64 ca 2b 23  3d a7 a5 79  │/···│·)d'│d·+#│=··y│
    00000120  77 0f 94 85  6e 4e a4 ab  b7 32 19 d6  84 14 b2 1d  │w···│nN··│·2··│····│
    00000130  72 35 50 3b  a6 15 89 0d  8e dc 38 85  ab 37 4f 16  │r5P;│····│··8·│·7O·│
    00000140  8d 16 5b 86  90 42 f6 43  66 d6 4a b5  b1 a9 da c8  │··[·│·B·C│f·J·│····│
    00000150  65 24 0e 8c  cd 7e 5b bb  cf c9 30 21  85 6c 85 c4  │e$··│·~[·│··0!│·l··│
    00000160  b8 3c 41 4d  dc 1e 51 a9  d5 92 b0 77  81 68 a5 03  │·<AM│··Q·│···w│·h··│
    00000170  13 52 c8 a6  c8 a2 b6 7b  7a b9 0c 74  eb 58 07 a2  │·R··│···{│z··t│·X··│
    00000180  fa cb dc f7  2a 06 85 14  b2 0f 32 f3  d2 c5 5c 15  │····│*···│··2·│··\·│
    00000190  5b c3 7e e0  59 d4 ac c3  f9 f8 16 a4  90 42 76 40  │[·~·│Y···│····│·Bv@│
    000001a0  42 5e 21 be  83 fd 54 0e  4f 62 c6 0b  58 16 83 b3  │B^!·│··T·│Ob··│X···│
    000001b0  54 84 42 0a  d9 11 c9 ea  0f 5b 21 4d  f7 16 aa 20  │T·B·│····│·[!M│··· │
    000001c0  3d 68 d2 f3  33 38 14 1c  42 0a d9 12  b9 f6 e7 56  │=h··│38··│B···│···V│
    000001d0  26 36 2b 05  62 11 5f 9e  70 91 c6 ec  26 a4 90 cd  │&6+·│b·_·│p···│&···│
    000001e0  90 58 df d1  1d b9 cb e0  c8 92 a6 cc  d2 8d 20 08  │·X··│····│····│·· ·│
    000001f0  4e f8 0f 19  52 48 21 7b  20 3d 7f a1  1d aa f7 48  │N···│RH!{│ =··│···H│
    00000200  e9 db b1 40  cc b3 58 11  8e 04 08 29  64 3f a4 c5  │···@│··X·│···)│d?··│
    00000210  fd 29 18 4c  5d a5 fa 2b  8c 87 13 5e  ec f0 21 a4  │·)·L│]··+│···^│··!·│
    00000220  90 1d 91 29  c8 b3 76 47  73 16 af 9b  aa f4 35 1e  │···)│··vG│s···│··5·│
    00000230  93 6e 84 90  42 b6 44 46  f5 c7 24 96  45 de c5 63  │·n··│B·DF│··$·│E··c│
    00000240  a2 dc ab 47  af 6b 25 02  a6 90 42 f6  43 ba 79 e7  │···G│·k%·│··B·│C·y·│
    00000250  26 78 64 2d  0b 78 9c c5  cd 68 aa 8a  3e 8f b7 20  │&xd-│·x··│·h··│>·· │
    00000260  85 14 b2 09  32 3d 08 36  55 8f 5c 75  6f 4d c9 95  │····│2=·6│U·\u│oM··│
    00000270  ea cf 33 59  c9 73 42 0a  d9 10 69 1b  a7 e5 7f 53  │··3Y│·sB·│··i·│···S│
    00000280  7c e4 66 cd  97 13 f3 5c  6a 56 48 21  5b 22 29 c8  │|·f·│···\│jVH!│[")·│
    00000290  22 be c3 38  c6 da e4 6b  61 3f 4c c2  b3 72 14 52  │"··8│···k│a?L·│·r·R│
    000002a0  c8 86 c8 5a  fd f9 32 c3  ef 41 f8 02  a1 f0 73 a7  │···Z│··2·│·A··│··s·│
    000002b0  6f 3c c3 84  14 b2 21 92  fb d7 ae 7b  c7 aa 08 69  │o<··│··!·│···{│···i│
    000002c0  de 95 ea 0f  f9 eb 66 a4  4d 31 43 9a  42 0a d9 0f  │····│··f·│M1C·│B···│
    000002d0  59 e4 35 3c  a7 61 f2 b2  b0 70 d3 13  0f c3 22 54  │Y·5<│·a··│·p··│··"T│
    000002e0  09 94 90 42  b6 42 42 63  21 cd e8 98  32 28 ad 6f  │···B│·BBc│!···│2(·o│
    000002f0  96 85 c6 56  ca c3 84 14  b2 2b 92 cb  48 53 6b 03  │···V│····│·+··│HSk·│
    00000300  ff a5 00 77  9c 6b ae d4  49 b9 62 7c  19 11 42 0a  │···w│·k··│I·b|│··B·│
    00000310  d9 03 b9 36  14 7b ce 1e  d9 8d a7 5e  14 e4 ac 1e  │···6│·{··│···^│····│
    00000320  84 d3 be 6c  3c 21 85 6c  82 a4 0c 33  6b 19 c2 8f  │···l│<!·l│···3│k···│
    00000330  c8 6e b1 85  1d 93 19 7f  89 90 42 36  46 e2 da d5  │·n··│····│··B6│F···│
    00000340  bf c1 7e 40  ae da ab f8  bc 0e 5c 3f  c2 f3 d7 b3  │··~@│····│··\?│····│
    00000350  40 14 52 c8  86 48 2a 10  0c d6 81 56  e0 7e 2a f4  │@·R·│·H*·│···V│·~*·│
    00000360  19 0e c5 ca  7d 86 58 21  85 ec 88 c4  bb 1d 35 5f  │····│}·X!│····│··5_│
    00000370  d2 50 11 ae  9a cf e8 7f  bf eb c5 13  2f 84 14 b2  │·P··│····│····│/···│
    00000380  23 f2 b5 4c  55 86 65 f7  3a 70 cf 3f  04 b1 04 9c  │#··L│U·e·│:p·?│····│
    00000390  34 f4 84 14  b2 19 12 46  5d 31 22 2e  1a 7a 5e 25  │4···│···F│]1".│·z^%│
    000003a0  a2 40 ac a9  8b 8d 16 ad  3d 0e 21 85  ec 85 24 03  │·@··│····│=·!·│··$·│
    000003b0  59 ab 78 dd  30 18 56 cd  c7 3a 70 a6  b5 47 b9 fe  │Y·x·│0·V·│·:p·│·G··│
    000003c0  e0 6d 08 29  64 17 a4 59  44 c6 d8 29  43 77 c2 8b  │·m·)│d··Y│D··)│Cw··│
    000003d0  07 71 7f b0  0e 64 3f f5  ce 90 42 0a  d9 03 f9 76  │·q··│·d?·│··B·│···v│
    000003e0  14 0e 16 7e  1e be de 8e  34 bc d9 54  b9 61 11 93  │···~│····│4··T│·a··│
    000003f0  90 42 76 44  e2 76 75 46  ae 62 63 64  9e dd 7c 2b  │·BvD│·vuF│·bcd│··|+│
    00000400  4a c0 d2 68  e1 e8 d0 a7  90 42 f6 43  3a 77 85 fb  │J··h│····│·B·C│:w··│
    00000410  ae 47 b3 e4  c9 2e ca 42  ac b9 52 57  24 eb 45 21  │·G··│·.·B│··RW│$·E!│
    00000420  85 6c 89 3c  23 e8 e5 db  2d 87 82 ed  15 04 19 05  │·l·<│#···│-···│····│
    00000430  e2 11 1d d8  f8 ca 90 42  0a d9 03 59  c3 77 7a e2  │····│···B│···Y│·wz·│
    00000440  f6 30 18 f2  11 fa f4 69  0b 1d 5f 42  0a d9 12 b9  │·0··│···i│··_B│····│
    00000450  de 21 39 65  77 e4 23 fd  3d f3 6f b0  24 78 2a dc  │·!9e│w·#·│=·o·│$x*·│
    00000460  08 7b 6b 5c  48 21 7b 20  b9 8c ac 45  69 5e c1 c0  │·{k\│H!{ │···E│i^··│
    00000470  a3 eb 13 c9  ee 32 66 41  ca 75 0a 29  64 43 a4 ab  │····│·2fA│·u·)│dC··│
    00000480  8d be 1d ea  bb 89 f6 0a  53 44 de e2  2b b5 e1 88  │····│····│SD··│+···│
    00000490  0b a6 21 a4  90 fd 90 18  14 df 74 bf  61 e7 fa e1  │··!·│····│··t·│a···│
    000004a0  47 22 6b 51  81 33 4e 35  cf 64 42 0a  d9 18 39 43  │G"kQ│·3N5│·dB·│··9C│
    000004b0  8b 91 c4 10  c4 b3 2a 0d  39 0d b4 28  1f 85 14 b2  │····│··*·│9··(│····│
    000004c0  17 d2 ac 48  6e 2b 5c e6  2f 1e 73 d0  74 a0 5c b3  │···H│n+\·│/·s·│t·\·│
    000004d0  d1 da a6 90  42 b6 44 8e  f5 91 8e c2  89 48 08 2d  │····│B·D·│····│·H·-│
    000004e0  ed 07 5e cf  16 7d 8e 59  27 21 85 6c  87 3c 01 b2  │··^·│·}·Y│'!·l│·<··│
    000004f0  91 7f 5f 60  59 98 72 c5  db 18 30 c1  cd 7e f4 36  │··_`│Y·r·│··0·│·~·6│
    00000500  84 14 b2 17  92 97 44 10  df 1a 3c 81  a6 c3 28 8f  │····│··D·│··<·│··(·│
    00000510  59 3e da 97  09 2e a4 90  bd 90 2e c3  ec 98 d6 f0  │Y>··│·.··│··.·│····│
    00000520  35 33 de c7  32 9d 51 86  57 49 6c 42  0a d9 0e b9  │53··│2·Q·│WIlB│····│
    00000530  3e 4e b6 52  96 cd 12 8b  c1 d4 a2 3f  5a 61 e0 40  │>N·R│····│···?│Za·@│
    00000540  21 85 6c 89  c4 d8 70 5d  04 05 22 d2  c7 c1 db a3  │!·l·│··p]│··"·│····│
    00000550  72 99 34 e9  e5 fd 20 48  21 85 ec 81  fc cd 21 a4  │r·4·│·· H│!···│··!·│
    00000560  90 42 0a 29  a4 90 42 0a  29 a4 90 42  0a f9 b7 90  │·B·)│··B·│)··B│····│
    00000570  ff 00 c4 47  e6 9d c1 07  72 13 00 00  00 00 49 45  │···G│····│r···│··IE│
    00000580  4e 44 ae 42  60 82                                  │ND·B│`·│
    00000586
10.
.- -. ... .-- . .-. / - .... . / ..-. --- .-.. .-.. --- .-- .. -. --. / --.- ..- . ... - .. --- -. / ---... / -.-. .- -. / -.-- --- ..- / - . .-.. .-.. / -- . / .-- .... .- - / -.-. --- .-.. --- .-. / .. ... / ---... / ----- --..-- ----- --..-- ..--- ..... .....
ANSWER THE FOLLOWING QUESTION : CAN YOU TELL ME WHAT COLOR IS : 0,0,255
can you tell me what color is : 0,0,255
Q4
0,0,255
[DEBUG] Sent 0x5 bytes:
    b'blue\n'
blue
[DEBUG] Received 0x38 bytes:
    b"You've done it ! The last flag is : ECW{R4ND0M_ST3G4N0}\n"
You've done it ! The last flag is : ECW{R4ND0M_ST3G4N0}

[*] Closed connection to instances.challenge-ecw.fr port 38082
```

## Python code
Complete solution in [sol.py](sol.py)

## Flags
- ECW{J1GS4W_R3TURNS}
- ECW{N0T_SC3R3D_Y3T}
- ECW{R4ND0M_ST3G4N0}
