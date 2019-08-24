```C++
auto c_xor = [](char _1) -> auto{
	return[_1](char _2)->auto{
		return (char)(_1^_2);
	};
};
```

这段代码实际上是**柯里化**，具体可以学习haskell，知乎上也有个专栏**从零开始学函数式C++**



```C++
puts("func(?)=\"01abfc750a0c942167651c40d088531d\"?");
```

这个去CMD5查要收费...换个站轻松查到是`#`字符的MD5值



代码中加入的time反调，最初是因为本题算法不复杂，angr几分钟就能跑出来

```C++
if(times > 0){
	puts("Let the silent second hand take the place of my doubt...");
	exit(0);
}
```



这里可以发现，times必须是0，也就是说数组下标中加上times不会有改变

```C++
for (int i = 1; i < 21; i++) {
	unsigned char c;
	c = input[i] ^ (char)times;
	c = c_add(c)(c_mod(input[i - 1 + times])(7));
	//c += flag[i - 1] % 7;
	c = c_xor(c)(c_add(c_mul(c_xor(input[i - 1 + times])(0x12))(3))(2));
	//c ^= (3 * (flag[i - 1] ^ 0x12) + 2);
	if (enc[i - 1] != c) {
		exit(0);
	}
}
```



由于最近在学ollvm，也用了fla参数，IDA看起来比较难受

```shell
~/build/bin/clang++ ./main.cpp -std=c++14 -mllvm -fla -o hardCpp
```





**exp**

```C
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

unsigned char enc[] = { 0xf3,0x2e,0x18,0x36,0xe1,0x4c,0x22,0xd1,0xf9,0x8c,0x40,0x76,0xf4,0x0e,0x00,0x05,0xa3,0x90,0x0e,0xa5 };

int main(int argc,char**argv){
	const char* flag = "#flag{mY-CurR1ed_Fns}";
	//MD5('#')="01abfc750a0c942167651c40d088531d"
	char dec[21] = { '#' };
	for (int i = 1; i < 21; i++) {
		char c = enc[i - 1];
		c ^= (3 * (dec[i - 1] ^ 0x12) + 2);
		c -= dec[i - 1] % 7;
		printf("%c", c);
		dec[i] = c;
	}
	return 0;
}
```



flag{mY-CurR1ed_Fns}