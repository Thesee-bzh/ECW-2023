# Reverse / Moth

## Challenge
Find the correct entry.

## Inputs:
- Binary: [moth](./moth)

## Solution
The binary is a stripped 64bit ELF:

```console
$ file moth
moth: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c4bae8f6969b8c00cbcef9cf356135434af7b1b2, for GNU/Linux 3.2.0, stripped
```

Let's open up `Ghidra` to analyse it:

Here is the main function below. Essentially:
- Takes a string as input
- Must have length 91 (0x51)
- `FUN_001011cd()` applied to the input string must report 0
- The flag is `ECW{md5(input)}` with the correct input string

```c
undefined8 FUN_001013dd(int param_1,long param_2)

{
  int iVar1;
  size_t sVar2;
  
  if (param_1 == 2) {
    sVar2 = strlen(*(char **)(param_2 + 8));
    if ((sVar2 == 0x51) && (iVar1 = FUN_001011cd(*(undefined8 *)(param_2 + 8)), iVar1 != 0)) {
      puts("Well done, flag is ECW{md5(input)}");
      return 0;
    }
    puts("Nope");
  }
  return 1;
}
```

Let's glance at FUN_001011cd() below (Ghidra's raw output, no cleanup). Essentially:
- Loop over every character `c` of the input string
- `c` must be between `a` and `e` (inclusive)
- Make 3 different checks on `c`
- If any failure on one of these checks, a flag is set (a bit in a bitmap)
- If no flag is set, function returns 0, which is what we want
- Also, the input string of 81 chars is considered a `square of 9*9 chars` (so it's basically parsed by chunks of 9 chars)

```c
bool FUN_001011cd(long param_1)

{
  char cVar1;
  char cVar2;
  int iVar3;
  uint local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  
  local_34 = 0;
  local_30 = 0;
  do {
    if (8 < local_30) {
      local_18 = 0;
      for (local_14 = 0; local_14 < 3; local_14 = local_14 + 1) {
        local_18 = local_18 + ((int)local_34 >> ((byte)local_14 & 0x1f) & 1U);
      }
      return local_18 == 0;
    }
    for (local_2c = 0; local_2c < 9; local_2c = local_2c + 1) {
      cVar1 = *(char *)(param_1 + (local_2c + local_30 * 9));
      if ((cVar1 < 'a') || ('e' < cVar1)) {
        return false;
      }
      cVar2 = (&DAT_00102020)[local_2c + local_30 * 9];
      iVar3 = FUN_00101169((int)cVar2);
      if (iVar3 < cVar1 + -0x60) {
        local_34 = local_34 | 1;
      }
      for (local_28 = 0; local_28 < 9; local_28 = local_28 + 1) {
        for (local_24 = 0; local_24 < 9; local_24 = local_24 + 1) {
          if ((((local_24 != local_2c) || (local_28 != local_30)) &&
              (cVar2 == (&DAT_00102020)[local_24 + local_28 * 9])) &&
             (cVar1 == *(char *)(param_1 + (local_24 + local_28 * 9)))) {
            local_34 = local_34 | 2;
          }
        }
      }
      for (local_20 = -1; local_20 < 2; local_20 = local_20 + 1) {
        for (local_1c = -1; local_1c < 2; local_1c = local_1c + 1) {
          if (((((-1 < local_1c + local_2c) && (-1 < local_20 + local_30)) &&
               ((local_1c + local_2c < 9 && (local_20 + local_30 < 9)))) &&
              ((local_1c != 0 || (local_20 != 0)))) &&
             (cVar1 == *(char *)(param_1 + (local_1c + local_2c + (local_30 + local_20) * 9)))) {
            local_34 = local_34 | 4;
          }
        }
      }
    }
    local_30 = local_30 + 1;
  } while( true );
}
```

First check below. Essentially:
- `input_string[i]` shall be less or equal to `DAT_00102020[i] + 0x60`
- for instance, if `DAT_00102020[i] = 2`, then `input_string[i]` shall be less or equal to 0x62 ('b')

```c
      cVar2 = (&DAT_00102020)[local_2c + local_30 * 9];
      iVar3 = FUN_00101169((int)cVar2);
      if (iVar3 < cVar1 + -0x60) {
        local_34 = local_34 | 1;
      }
```

Second check below. Essentially:
- `input_string[i]` shall be different to `input_string[j]` in case `D[i]` is equal to `D[j]`
- for instance `input_string[0]` shall be different to `input_string[1]` because `D[0] = D[1] = 1`

```c
      for (local_28 = 0; local_28 < 9; local_28 = local_28 + 1) {
        for (local_24 = 0; local_24 < 9; local_24 = local_24 + 1) {
          if ((((local_24 != local_2c) || (local_28 != local_30)) &&
              (cVar2 == (&DAT_00102020)[local_24 + local_28 * 9])) &&
             (cVar1 == *(char *)(param_1 + (local_24 + local_28 * 9)))) {
            local_34 = local_34 | 2;
          }
        }
      }
```

Third check below. Sounds complicated, but essentially:
- The representation of a 9*9 square comes into play
- In this representation, every neighors of `input_string[i]` shall be different from `input_string[i]`
- Also applies to borders and corners !
```c
      for (local_20 = -1; local_20 < 2; local_20 = local_20 + 1) {
        for (local_1c = -1; local_1c < 2; local_1c = local_1c + 1) {
          if (((((-1 < local_1c + local_2c) && (-1 < local_20 + local_30)) &&
               ((local_1c + local_2c < 9 && (local_20 + local_30 < 9)))) &&
              ((local_1c != 0 || (local_20 != 0)))) &&
             (cVar1 == *(char *)(param_1 + (local_1c + local_2c + (local_30 + local_20) * 9)))) {
            local_34 = local_34 | 4;
          }
        }
      }
```

Now that we understand all the constraints of the problem, we'll use `z3` SAT solver to solve it.

```python
from z3 import *
from hashlib import md5

D = [ 0x01, 0x01, 0x01, 0x01, 0x02, 0x03, 0x03, 0x04, 0x05, 0x06, 0x01, 0x07, 0x02, 0x02, 0x03, 0x04, 0x04, 0x05, 0x06, 0x07, 0x07, 0x07, 0x02, 0x02, 0x08, 0x04, 0x05, 0x06, 0x07, 0x09, 0x09, 0x09, 0x09, 0x08, 0x04, 0x05, 0x06, 0x0a, 0x09, 0x0b, 0x0b, 0x08, 0x08, 0x08, 0x0d, 0x0a, 0x0a, 0x0a, 0x0c, 0x0b, 0x0b, 0x0e, 0x0d, 0x0d, 0x0a, 0x0f, 0x0f, 0x0c, 0x0b, 0x0e, 0x0e, 0x0e, 0x0d, 0x10, 0x0f, 0x0f, 0x0f, 0x12, 0x13, 0x13, 0x13, 0x0d, 0x10, 0x10, 0x11, 0x12, 0x12, 0x12, 0x12, 0x13, 0x13 ]

N = 81
```

Rule for first condition (including the condition for `c` to be between `a` and `e`):
```python
s = Solver()
s.add( [ And(S[i] >= ord('a'), S[i] <= ord('e'), S[i] <= D.count(D[i]) + 0x60) for i in range(N) ])
```

Rule for second condition. The prerequisite here is to build lists of positions in the input string which share the same value in `D`:
```python
# Build list of indexes in D sharing same value
L = []
for i in range(0x1, 0x14):
    l = [ x for x in range(len(D)) if D[x] == i ]
    if len(l) > 1:
        L.append(l)

s.add( [ Distinct([ S[i] for i in l]) for l in L ])
```

Rule for third condition. The prerequisite here is to build lists of position neighbors in the `9*9 square`, for each position. This applies to borders and corners as well. So for instance:
- Position 0 (upper left corner of the 9*9 square): position neighbors = [1, 9, 10]
- Position 1 (on upper border): position neighbors = [0, 2, 9, 10, 11]
- Position 10 (in the middle): position neighbors = [0, 1, 2, 9, 11, 18, 19, 20]

```python
# Build list of neighbors in a 9*9 square (mind the borders and corners !)
L_ = [ [] for i in range(N) ]
for i in range(9):
    for chunk in range(9):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if ((-1 < k + i)
                    and (-1 < j + chunk)
                    and (k + i < 9)
                    and (j + chunk < 9)
	            and (k != 0 or j != 0)):
                    L_[i+9*chunk].append(k + i + (chunk + j) * 9)

s.add( [ And( [ S[i] != S[neighbor] for neighbor in L_[i] ] ) for i in range(N) ] )
```

Finally, we request `z3` to solve the problem, and craft the flag as requested (using `hashlib.md5()`) if we get a solution:
```python
# Solve the problem
if s.check() == sat:
    # We have a solution !
    m = s.model()
    r = [m.evaluate(S[i]) for i in range(N)]
    m = ''.join([chr(i.as_long()) for i in r])
    print(m, '\n')
    # Show it as a 9*9 square
    chunks = [m[i:i+9] for i in range(0, len(m), 9)]
    for chunk in chunks:
        print(chunk)
    # Craft flag as requested
    print("\nECW{", md5(m.encode()).hexdigest(), "}", sep='')
```

Fingers crossed... It does find a solution !
```console
$ python3 sol.py
bcaedbabaadbcacdcdbcadbebabdebecaceccadadedabdbebcbcedcacaedababebdbcedcacacedaba

bcaedbaba
adbcacdcd
bcadbebab
debecacec
cadadedab
dbebcbced
cacaedaba
bebdbcedc
acacedaba

ECW{8b39553c944cdce4ea4f9a692168093b}
```
And we can verify that the solution is correct using the binary:
```console
$ ./moth bcaedbabaadbcacdcdbcadbebabdebecaceccadadedabdbebcbcedcacaedababebdbcedcacacedaba
Well done, flag is ECW{md5(input)}
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
ECW{8b39553c944cdce4ea4f9a692168093b}
