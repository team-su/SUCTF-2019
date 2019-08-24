#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#include<iostream>
#include<functional>
using namespace std;

unsigned char enc[] = { 0xf3,0x2e,0x18,0x36,0xe1,0x4c,0x22,0xd1,0xf9,0x8c,0x40,0x76,0xf4,0x0e,0x00,0x05,0xa3,0x90,0x0e,0xa5 };

int main(int argc, char**argv) {
	int t1 = time(NULL);

	auto c_xor = [](char _1) -> auto{
		return[_1](char _2)->auto{
			return (char)(_1^_2);
		};
	};

	auto c_add = [](char _1)->auto{
		return[_1](char _2)->auto{
			return (char)_1 + _2;
		};
	};

	auto c_mul = [](char _1)->auto{
		return[_1](char _2)->auto {
			return (char)_1 * _2;
		};
	};

	auto c_mod = [](char _1)->auto{
		return[_1](int _2)->char {
			return _1 % _2;
		};
	};

	char input[22];
	puts("func(?)=\"01abfc750a0c942167651c40d088531d\"?");
	//MD5('#')
	input[0] = getchar();

	fgets(input + 1, 21, stdin);
	int t2 = time(NULL);

	int times = t2 - t1;

	if (times > 0) {
		puts("Let the silent second hand take the place of my doubt...");
		exit(0);
	}


	int len = strlen(input);
	if (len != 21) {
		exit(0);
	}


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

	puts("You win");
	return 0;
}
