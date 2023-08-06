# radix-ops

Convert numbers - both integer and floating-point - from one base to another.
Perform arithmetic operations in a given base.

### Installation

```Shell
pip install radix-ops
```

### Usage

```Python
from radix import Num

a = Num(20, 16)    # The number 20 in base 16
print(a.to(2))     # Convert to base 2 (100000)

a = Num(20, 16)
b = Num('ff', 16)  # FF or 255 in base 16
print(a + b)       # Result in base 16 (11F)
```
An easier way to evaluate expressions:

```Python
from radix import expr

# All numbers in base 16. result is a `Num` instance.
result = expr('a + b * c', 16)

print(result)  # prints 8E
print(result.to(10))  # prints 142
```
#### (Signed) binary numbers

```Python
>>> from radix import Bin  # `Bin` is a subclass of `Num`
>>> num = Bin(-7)
>>>
>>> # -ve number in 2's complement
>>> num
1001
>>> num.twos_compl()  # 2's complement
'1001'
>>> num.ones_compl()  # 1's complement
'1000'
>>> num.format(size=8, blanks_every=4)  # format 2's complement
'1111 1001'
>>> num.sign_mag()  # sign magnitude representation
'1111'
>>>
>>> # -10 in 2's complement
>>> Bin(-5) + Bin(3) - Bin(8)  # 2's complement arithmetic
10110

```
## Examples

```Python
>>> from radix import Num, expr
>>> Num(value='FE', base=16).to(base=10)
254
>>> Num(1100, 2).to(10)
12
>>> Num(10.75).to(16)  # When base is 10, it can be omitted.
A.C
>>> Num(10.75).to(2)
1010.11
>>> pi = 3.141592653589793
>>> Num(pi).to(16)
3.243F6A8885
>>> Num(-1001, 2).to(10)
-9
>>> (Num('1a', 16) - Num('ff', 16)) * Num(2, 16)  # (26 - 255) * 2 = -458 = -0x1ca
-1CA
>>> expr('-fe', 16, show=True).to(10)
-Num('fe', 16)
-254
>>> expr('b / (a + 1.5) * 2', 12)
1.B15A50B68B
>>> from radix import dim_radix_compl, radix_compl
>>> dim_radix_compl(Num('012398'))  # 9's complement (diminished radix complement)
'987601'
>>> radix_compl(Num('012398'))  # 10's complement (radix complement)
'987602'

```

### Note

1. Base should be between 2 and 36.

2. The `.to` method mutates the number, i.e. changes its value and base. 

3. Very large or very small floating-point numbers should be in quotes.
