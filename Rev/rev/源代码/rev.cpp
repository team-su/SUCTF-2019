#include<iostream>
#include<string>
#include<windows.h>
#include<boost/typeof/typeof.hpp>
#include<boost/tokenizer.hpp>
#include<boost/algorithm/string/trim.hpp>
#include<boost/algorithm/string/predicate.hpp>
#include<boost/algorithm/string/case_conv.hpp>

int func(int num) {
	num *= 1234;
	num += 5678;
	num /= 4396;
	num ^= 0xabcddcba;
	num -= 8888;
	return num;
}

int func2(int num) {
	num *= 2334;
	num += 9875;
	num /= 7777;
	num ^= 0x12336790;
	num -= 4431;
	return num;
}

int main(int argc, char** argv) {
	std::string input;
	std::cin >> input;
	boost::tokenizer<> tok(input);
	int count = 0;
	std::string res[5];
	for (BOOST_AUTO(pos, tok.begin()); pos != tok.end(); ++pos) {
		res[count] = *pos;
		count++;
	}
	if (count != 3) {
		_exit(count);
	}

	//输入形如aaaa-bbb-cc

	//check res[0]，前面5个1,后面5个字符suctf
	//11111suctf
	if (res[0].length() != 10) {
		_exit(res[0].length());
	}
	std::string res1_trim = boost::trim_left_copy_if(res[0], boost::is_any_of("1"));
	unsigned char chars[6] = { 0xd8,0xde,0xc8,0xdf,0xcd };
	int i = 0;
	for (i = 0; i < res1_trim.length(); i++) {
		if ((unsigned char)(res1_trim[i] ^ 0xab) != chars[i]) {
			Sleep(1000000000000);
			_exit(0);
		}
		else {
			printf("%c", res1_trim[i]);
		}
	}
	if (i != (count + 2)) {
		_exit(1);
	}



	//check res[1]
	//res[1]都输入[a-gA-G]，长度为4
	int flag = 0;
	if ((res[1].length() == 4) && (boost::all(res[1], boost::is_from_range('a', 'g') || boost::is_from_range('A', 'G')))) {
		std::string res2_to_upper(res[1]);
		boost::to_upper(res2_to_upper);

		//表明要输入的都是大写字符
		if (res[1] == res2_to_upper) {
			//递增步长为2,ACEG
			for (int i = 0; i < res2_to_upper.length() - 1; i++) {
				if ((res2_to_upper[i] + 2) != (res2_to_upper[i + 1])) {
					flag = 1;
				}
			}
		}
		else {
			flag = 1;
		}

	}
	else {
		flag = 1;
	}

	if (flag) {
		std::cout << "You lost sth." << std::endl;
		system("pause");
		return 0;
	}
	else {
		std::cout << "{" << res[1];
	}


	//check res[2]
	int sum = 0;

	if ((res[2].length() < 10) && (boost::all(res[2], boost::is_digit()))) {
		for (auto c : res[2]) {
			sum *= 10;
			sum += (c - '0');
		}
	}
	else {
		return 3;
	}
	if ((sum % 2 == 0) && (func(sum) == -1412590079) && (func2(sum) == 305392417)) {
		std::cout << sum << "}" << std::endl;
	}


	std::cout << "You win!" << std::endl;
	return 0;
}