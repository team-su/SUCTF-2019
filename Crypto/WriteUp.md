##	Crypto
### DSA

#### 出题思路

该题的漏洞点在于DSA数字签名方案中的随机数k的唯一性，随机数k在DSA数字签名中起到了类似于时间戳的作用。一旦两次签名中的k相同，就会造成私钥泄露。因此本题在给出的若干条消息签名中，故意使用重复的随机数k。

###    解题思路

##### DSA数字签名

##### 签名方案

1. 选定公共参数$p,q,g$，其中$g^q \bmod p=1$，即$g$的阶为$p$；
2. 签名方随机生成私钥$x$，满足$0<x<q$，计算并公开公钥$y=g^x \bmod q$
3. 针对消息$m$，起算其哈希值$h=H(m)$，并生成随机数$k$，满足$0<k<q$；
4. 计算$r=(g^k \bmod p) \bmod q$；（相当于时间戳，防止重放攻击）
5. 计算$s=k^{−1}(H(m)+xr) \bmod q$；
6. 以$<r,s>$为数字签名。

##### 验签方案

接收方在已知公共参数$p,q,g$和接收到消息$m$与签名$<r,s>$的基础上，可以通过验证以下等式是否成立来验证签名是否有效。
$$
r=(g^{s^{-1}H(m)}+y^{s^{-1}r} \bmod p) \bmod q
$$
其中$s^{-1}$指$s$在模$q$时的乘法逆元。

##### 利用方法

一旦发现两条消息$m_1,m_2$的数字签名$<r_1, s_1>$和$<r_2,s_2>$有$r_1=r_2=r$，则说明它们在签名过程中使用了相同的随机数$k$。根据签名方案有：
$$
ks_1=H(m_1)+xr \bmod q\\
ks_2=H(m_2)+xr \bmod q
$$
因此有
$$
xr(s_2-s_1)\equiv H(m_2)s_1-H(m_1)s_2 \pmod q
$$
所以
$$
x=(r(s_2-s_1))^{-1}(H(m_2)s_1-H(m_1)s_2) \bmod q
$$
求得私钥$x$后，自然可以根据DSA数字签名方案对任意消息进行签名。

##### exp

略。

### Prime

####    出题思路

对任意两个不同素数$p,q$和整数$n=pq$，对任意整数$m,0<m<p$且$m<q$，若$c=m^n \bmod n$，则
$$
c^{q'} \bmod q= m
$$
其中$q'$满足$q' \cdot p \bmod (q-1) = 1$。

**证明**：$c^{q'} \bmod q=m^{nq'} \bmod q=m^{qpq'} \bmod q=m^{((q-1)+1)(k(q-1)+1)} \bmod q=m^{k'(q-1)+1} \mod q$

根据费马小定理：$m^{q-1} \bmod q=1$，所以$m^{k'(q-1)+1} \mod q=m$。

同理$c^{q'} \bmod p= m$。

本题在该结论的基础上做了进一步扩展。

1. 将素数数量由2个扩大到4个；
2. 将$m$的范围扩大到$0<m<n$

#### 解题思路

1.对给出的$n_0,n_1,n_2,n_3$做最大公因子分析，可分别得出他们的四个素因子；

2.一般的，对$n=p_1p_2p_3p_4$和$c=m^n \bmod n$，有
$$
c^{{p_i}'}\equiv m \pmod {p_i}
$$
其中${p_i}'$满足${p_i}' \cdot \frac n {p_i} \bmod (p_i-1) = 1$，即${p_i}'$是$\frac n {p_i}$在模$ (p_i-1) $的乘法逆元。

3.利用中国剩余定理求解$m$。

#### exp

```python
import numpy as np
import gmpy2 as gm
def crack(N, ns, cs):
    M = np.ones((N, N))
    M = M.tolist()
    for i in range(N):
        M[i][i] = 1
        for j in range(N):
            if i != j:
                M[i][j] = gm.gcd(ns[i], ns[j])
                M[i][i] *= M[i][j]
        M[i][i] = ns[i] / M[i][i]

    nsns = [1] * 4
    for i in range(N):
        for j in range(N):
            nsns[i] *= M[i][j]

    index = np.ones((N, N))
    index = index.tolist()

    for i in range(N):
        for j in range(N):
            index[i][j] = 1
            for k in range(N):
                if k != j:
                    index[i][j] *= gm.invert(M[i][k], M[i][j] - 1)

    cc = np.ones((N, N))
    cc = cc.tolist()
    for i in range(N):
        for j in range(N):
            cc[i][j] = pow(cs[i], index[i][j], M[i][j])

    mms = [0] * N
    for i in range(N):
        for j in range(N):
            fac = cc[i][j]
            for k in range(N):
                if k != j:
                    fac *= (M[i][k] * gm.invert(M[i][k], M[i][j]))
            mms[i] += fac % ns[i]
        mms[i] = mms[i] % ns[i]
    return mms
```

### MT

#### 出题思路

随机数发生器MT19937在从状态提取32bits随机数时进行四步平移和异或运算，但该四步运算均为可逆运算，从而导致可从32bits随机数还原状态。

```python
...
def extract_number(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640d
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18
        self.index = self.index + 1
        return _int32(y)
...
```

本题将这四步运算的参数略作调整，考察选手能否对其进行逆运算。

#### 解题思路

分别实现左移和右移异或的逆运算函数，然后调用两个函数对密文解密，得到flag。代码如下。

```python
from Crypto.Util import number

transformed_flag = '641460a9e3953b1aaa21f3a2'
c = transformed_flag.decode('hex')

def decrypt_left(cipher, blocksize, mask):
    plain = cipher
    t = cipher
    for i in range(32 / blocksize):
        tt = (t << blocksize) & mask
        plain = plain ^ tt
        t = tt
    return plain

def decrypt_right(cipher, blocksize, mask):
    plain = cipher
    t = cipher
    for i in range(32 / blocksize):
        tt = (t >> blocksize) & mask
        plain = plain ^ tt
        t = tt
    return plain

def invert(block):
    block = decrypt_right(block, 19, 0xffffffff)
    block = decrypt_left(block, 17, 2245263360)
    block = decrypt_left(block, 9, 2029229568)
    block = decrypt_right(block, 13, 0xffffffff)
    return block

def transform(message):
    assert len(message) % 4 == 0
    new_message = ''
    for i in range(len(message) / 4):
        block = message[i * 4 : i * 4 +4]
        block = number.bytes_to_long(block)
        block = invert(block)
        block = number.long_to_bytes(block)
        new_message += block
    return new_message

flag = transform(c)
print flag.encode('hex')
```

### RSA

#### 出题思路

该题考察对RSA的parity oracle或LSB oracle漏洞的利用。网上关于parity oracle漏洞利用的writeup和脚本很多，大多是这样的：

```python
def crack(n, e, c):
    max = n
    min = 0
    d = pow(2, e, n)
    cc = c
    while True:
        cc = (cc * d) % n
        parity = getParity(cc) #parity oracle返回明文奇偶性
        if parity == 1:
            min = (max + min) / 2
        else:
            max = (max + min) / 2
        if max == min:
            return min
```

原理很简单，但一般情况下最终还原出的明文和真实明文会存在一定偏差，主要原因是max和min是整数类型，其表示的上界和下界不够精确；提高表示精度可以一定程度解决这个问题，但治标不治本，理论上还是存在误差导致还原出的明文不准确。为了增加这种误差存在的概率，原题设置为2048位的$n$，并且要破解10个$m$，后考虑到与服务器交互次数过多，破解时间过长而将参数降低到1024和3。

####    解题思路

这里仅给出精确还原的脚本，其正确性和完备性证明可参见[A Novel Algorithm for Exploiting RSA Plain’s LSB Oracle][1]。

```python
def crack(n, e, c):
    rounds = int(math.ceil(math.log(n, 2)))
    d = pow(2, e, n)
    cc = c
    eigenvalue = 0
    for i in range(rounds):
        if i % 256 == 0:
            print i
        cc = (cc * d) % n
        parity = getParity(cc) #parity oracle返回明文奇偶性
        eigenvalue = (eigenvalue << 1) + parity
    if eigenvalue == 0:
        return 0
    else:
        return n * eigenvalue / pow(2, rounds) + 1
```