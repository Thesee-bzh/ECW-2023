from pwn import *
import base64
from webcolors import rgb_to_name, IntegerRGB
from PIL import Image
import io
import zxingcpp
from pybraille import convertText

resp_l = []

Q1 = b"1. Do you wanna play a game?"
Q2 = b"2. What is the meaning of life, the universe, and everything, according to Deep Thought?"
Q3 = b"3. Easy question, Which letter comes "
Q4 = b"4. Can you tell me what color is : "
Q5 = b"5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas."
Q6 = b"6. I did not understand. Can you repeat your previous answers for question(s) "
Q7 = b"7. Just to be sure it wasn't luck, random question time : "
Q8 = b"8. " # Then some Morse/Braille code...
Q9 = b"9. " # Then a PNG image with plaintext
Q10 = b"10. " # Then a PNG image with Morse/Braille code
Q11 = b"Please give your username for the leaderboard"

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

def q1(random=False):
    # Q1 = b"1. Do you wanna play a game?\n"
    if not random:
        c.recvuntil(Q1); print(Q1.decode())
    resp = b"yes"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q2(random=False):
    # Q2 = b"2. What is the meaning of life, the universe, and everything, according to Deep Thought?\n"
    if not random:
        c.recvuntil(Q2); print(Q2.decode())
    resp = b"42"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q3(random=False, req=None):
    # Q3 = b"3. Easy question, Which letter comes "
    if not random:
        c.recvuntil(Q3); print(Q3.decode())
        req = c.recvline().strip()
    if b"before" in req:
        op = -1
    else:
        op = +1
    print(req.decode())
    resp = chr(req[-1]+op).encode()
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q4(random=False, req=None):
    # Q4 = b"4. Can you tell me what color is : "
    if not random:
        c.recvuntil(Q4); print(Q4.decode())
        req = c.recvline().strip()
    else:
        req = req.decode().split(': ')[1].encode()
    print(req.decode())
    rgb = req.decode().split(',')
    l = [int(rgb[0]), int(rgb[1]), int(rgb[2])]
    color = tuple(l)
    resp = rgb_to_name(color).encode()
    if resp == b'lime':
        resp = b'green'
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q5(random=False):
    # Q5 = b"5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas."
    if not random:
        try:
            c.recvuntil(Q5); print(Q5.decode())
        except:
            return False
    resp = resp_l[0] + b',' + resp_l[1] + b',' + resp_l[2] + b',' + resp_l[3]
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True

def q6(random=False, req=None):
    # Q6 = b"6. I did not understand. Can you repeat your previous answers for question(s) "
    if not random:
        try:
            c.recvuntil(Q6); print(Q6.decode())
        except:
            return False
        req = c.recvuntil(b"using the same format ?")
    req = req.decode().split(" using")[0].split(',')
    print(req)
    req_l = [int(x) for x in req]
    resp = b''
    for i in range(len(req_l)):
        resp += resp_l[req_l[i] - 1]
        if (i != len(req_l) - 1):
            resp += b','
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True

def q7(skip=False, req=None):
    # Q7 = b"7. Just to be sure it wasn't luck, random question time : "
    if not skip:
        try:
            c.recvuntil(Q7); print(Q7.decode())
        except:
            return False
        req = c.recvline().strip().lower()
    print(req.decode())
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
    return True

def to_morse(s):
    return ' '.join(MORSE_CODE.get(i.upper()) for i in s)

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

def q11(random=False):
    # Q11 = b"Please give your username for the leaderboard"
    if not random:
        c.recvuntil(Q11); print(Q11.decode())
    resp = "Thésée".encode()
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def quizz():
    q1()
    q2()
    q3()
    q4()
    if q5() == False:
        return False
    if q6() == False:
        return False
    if q7() == False: # Q7: random question !
        return False
    if q8() == False:
        return False
    if q9() == False:
        return False
    q10()
    return q11()

def main():
    global c # Burk...
    c = remote("instances.challenge-ecw.fr", 38229)
    ret = quizz()
    if ret == True:
        return
    c.close()

main()
print(c.recvline().decode())
    
