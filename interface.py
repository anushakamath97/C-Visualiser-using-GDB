'''
to run:
gcc -g try.c
python gdb_new.py
Enter file :a.out
'''

'''
parameter passing?
info frame

return value?
finish

global variables
'''

from subprocess import *
import subprocess
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import string

y = 0
ret = 0

file = raw_input('enter program name (with a ./ if in local directory): ')

p1 = Popen(['gdb', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

flags = fcntl(p1.stdout, F_GETFL) # get current p.stdout flags
fcntl(p1.stdout, F_SETFL, flags | O_NONBLOCK)

def output(p1,flag):
	my_out = ''
	sleep(0.3)
	while True:
		try:
			my_out = read(p1.stdout.fileno(), 1024)
		except OSError:
			# the os throws an exception if there is no data
			# print '[No more data]'
			break
	#print my_out
	if 'result = 0' in my_out:
		global y
		y = 1
		return
	if 'Value returned is' in my_out:
		global ret
		my_out = my_out.split(' ')
		print 'Return Value:',my_out[len(my_out)-2].split('\n')[0],'\n'
		ret = 0
		return
	if 'return' in my_out:
		global ret
		ret = 1
		#print my_out
		return 
	if flag == 2:
		my_out = string.replace(my_out,'(gdb)','')
		my_out = my_out.split(' ')
		my_out = my_out[:2]
		print ' '.join(my_out)
	elif flag == 1:
		my_out = string.replace(my_out,'(gdb)','')
		print '(Stack Frame)'
		print my_out
p1.stdin.write('break main\n')
output(p1,0)
p1.stdin.write('run\n')
output(p1,0)

while True:
	p1.stdin.write('step\n')
	output(p1,0)
	if y == 1:
		break
	if ret == 1:
		p1.stdin.write('finish\n')
		output(p1,3)
	p1.stdin.write('info line\n')
	output(p1,2)
	p1.stdin.write('info locals\n')
	output(p1,1)

