#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <stdlib.h>
#include <malloc.h>

#define nullptr    0
using namespace std;
char buf[200];


/* purecall add start */

class base {
public:
	char* str;
	base() {
		this->str = (char*)malloc(32);
		memcpy(this->str, "hello,world", 32);
	}
	~base() {
		puts(this->str);
		free(this->str);
		this->str = nullptr;
	}
};

class derived :public base {
public:
	char* flag;
	derived() {
		this->flag = nullptr;
	}
	derived(char* s) {
		this->flag = s;
	}

	~derived() {
		this->flag = nullptr;
	}
};


/* purecall add end */

int Get_return_addr() {
	int re_addr;
	asm(
		"mov (%%ebp),%%eax\n\t"
		"mov 4(%%eax),%%eax\n\t"
		: "=r"(re_addr)
	);
	return re_addr;
}

void do_fmt() {
	while (1) {
		read(0, buf, 200);

		if (!strncmp(buf, "quit", 4))
			break;
		printf(buf);
	}
	return;
}

void logo() {
	const int logo_ret = Get_return_addr();
	puts("=====================");
	puts("  Magic echo Server");
	puts("=====================");
	do_fmt();
	if(logo_ret != Get_return_addr())
		exit(0);
	return;
}



int main() {
	char *flag = (char *)malloc(0x10);	//flag指针
	FILE *fd = fopen("flag.txt","r");
	if(!fd){
		printf("open flag error , please contact the administrator!\n");
		exit(0);
	} 
	fscanf(fd , "%s" , flag);
	fclose(fd);
	puts("Testing my C++ skills...");
	
	
	//安全操作

	puts("testing 1...");
	derived* nothing = new derived(nullptr);
	delete nothing;

	puts("testing 2...");
	derived* nothing2 = new derived();
	delete nothing2;

	puts("testing 3...");
	//漏洞点

	//带参构造函数，this->flag = (global)flag
	derived* ptr = new derived(flag);
	base* ptr2 = (base*)ptr;
	puts("You think I will leave the flag?");
	
	delete ptr2;	//资源泄露

	flag = nullptr;
	//防止printf里直接打印这个栈上局部变量

	const int main_ret = Get_return_addr();
	setvbuf(stdout, 0, 2, 0);
	logo();
	if (main_ret != Get_return_addr())
		exit(0);
	return 0;
}

