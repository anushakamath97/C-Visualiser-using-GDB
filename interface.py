'''
to run:
python interface.py
Enter file :<name of your c program to be visualised>
'''

'''
To be done:
heap
proper visualisation
'''

from subprocess import *
import subprocess
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import string
import re
import sys

sep = ['+','-','=','*','/',';','[','.']
global_name_list = []
stop = 0
ret = 0
scanf = 0
func = re.compile("\w+ \(((\w+\=\w+), )*(\w+\=\w+)?\)")

my_file = raw_input('Enter C program name (with a ./ if in local directory): ')

subprocess.call(["gcc","-g","-static",my_file])

p_glob = Popen(['gdb', 'a.out'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p_glob.stdin.write('info variables\n')
op = p_glob.communicate()
glob_list = op[0].split('\n')

i = glob_list.index('File '+my_file+':') + 1
while glob_list[i]!='':
	x = glob_list[i].split(' ')[1].replace(";",'').replace("\n",'')
	if x[0] == '*':
		x = x[1:]
	name = ''
	for j in range(0,len(x)):
		if x[j] in sep:
			break
		name = name + x[j]
	global_name_list.append(name)
	i += 1
#print global_name_list


p1 = Popen(['gdb', 'a.out'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

flags = fcntl(p1.stdout, F_GETFL) # get current p.stdout flags
fcntl(p1.stdout, F_SETFL, flags | O_NONBLOCK)

print 'Hit Enter to Begin'
def output(p1,flag):
	my_out = ''
	sleep(0.1)
	while True:
		try:
			my_out = read(p1.stdout.fileno(), 1024)
		except OSError:
			# the os throws an exception if there is no data
			# print '[No more data]'
			break
	#print "-------------------------------------------------"
	#print my_out
	#print "-------------------------------------------------"
	if "scanf" in my_out:
		global scanf
		scanf = 1
	if "printf" in my_out:
		print "Output from printf is:"
		op_string = my_out[11:len(my_out)-9].split(",")
		i = 0
		i_args = 1
		format_string = op_string[0]
		format_string = string.replace(format_string,'"','')
		while i<len(format_string):
			if format_string[i] == '%':
				temp = 'print '+op_string[i_args]+'\n'
				p1.stdin.write(temp)
				output(p1,5)
				i_args += 1
				i +=2
				continue
			sys.stdout.write(format_string[i])
			i += 1
		print '\n'		
	global ret
	m = func.match(my_out)
	#print m
	#print my_out
	if m is not None:
		my_out = m.group()
		func_name,my_out = my_out.split('(')
		my_out = my_out.split(')')[0]
		my_out = my_out.split(',')
		print "Function ",func_name," called with arguments:"
		for arg in my_out:
			print arg.strip()
		print "\n"
		return
	if 'result = 0' in my_out:
		global stop
		stop = 1
		return
	if 'Value returned is' in my_out:
		my_out = my_out.split(' ')
		print 'Return Value:',my_out[len(my_out)-2].split('\n')[0],'\n'
		ret = 0
		return
	if 'return' in my_out:
		ret = 1
		return 
	if flag == 6:
		my_out = my_out.split('=')[1]
		my_out = string.replace(my_out,'(gdb)','')
		my_out = string.replace(my_out,'\n','')
		sys.stdout.write(my_out+'\n')
	if flag == 5:
		#print my_out
		my_out = my_out.split('=')[1]
		my_out = string.replace(my_out,'(gdb)','')
		my_out = string.replace(my_out,'\n','')
		sys.stdout.write(my_out)
	elif flag == 2:
		my_out = string.replace(my_out,'(gdb)','')
		my_out = my_out.split(' ')
		my_out = my_out[:2]
		print ' '.join(my_out)
	elif flag == 1:
		my_out = string.replace(my_out,'(gdb)','')
		print '\n(Stack Frame)'
		print my_out
	elif flag == 4:
		my_out = string.replace(my_out,'(gdb)','').strip()
		if my_out != "No arguments.":
			print "(Arguments)"
			print my_out
			print "\n"
			

p1.stdin.write('break main\n')
output(p1,0)
p1.stdin.write('run\n')
output(p1,0)

while True:
	inp = raw_input()
	if(inp=='exit' or inp=='quit' or inp=='q'):
		break
	p1.stdin.write('step\n')
	if scanf == 1:
		print "Enter input for scanf:\n"
		p1.stdin.write(str(input())+'\n')
		scanf = 0
	output(p1,0)
	p1.stdin.write('info line\n')
	output(p1,2)
	print '(Global Variables)'
	for i in global_name_list:
		sys.stdout.write(i+" = ")
		p1.stdin.write('print '+i+'\n')
		output(p1,6)
	p1.stdin.write('info locals\n')
	output(p1,1)
	p1.stdin.write('info args\n')
	output(p1,4)
	if stop == 1:
		break
	if ret == 1:
		p1.stdin.write('finish\n')
		output(p1,3)
	print 'Hit Enter to Continue, exit/quit to stop\n'
	
	

