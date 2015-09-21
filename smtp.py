import argparse
import getpass
import sys
import telnetlib

parser=argparse.ArgumentParser(description='Verify usernames through SMTP RCPT commands')
parser.add_argument('-a', help="specify target host address", dest="host")
parser.add_argument('-p', help="specify port (default is 25)", dest="port")
parser.add_argument('-U', help="list of possible usernames", dest="users_file")
parser.add_argument('-v', help="enable verbosity",
 action="store_true", dest="verbose")
parser.add_argument('-o', help="output file", dest="output")

args=parser.parse_args()
#one potential check for arguments
if ((args.host is None) or (args.users_file is None)): 
	print "Error, use the -h help to learn more about this script"
	parser.print_help()
	sys.exit(1)

host=args.host
if (args.port is None):
	port=25
else:
	port=args.port
users_file=args.users_file
#Telnet in using the arguments
tn = telnetlib.Telnet(host,port)
tn.write("helo x" + "\n")
tn.write("mail from: roguer@slax.example.net" + "\n")
 
#we wait for the Sender ok command
print "SMTP verification -- Username check in progress please wait.."
print tn.read_until("Sender ok",120)
inp = open(users_file,"r")
#we check usernames one by one to see if they are unknown or not
#250 is code for OK , 550 is code for Unknown
temp=""
output=[]
for linea in inp.readlines():
	tn.write("rcpt to: "+ linea)
	temp = tn.read_until("Recipient ok",0.05)
	if (args.verbose):
		print temp
	output.append(temp)
inp.close()
tn.write("quit" + "\n")
print "--------------------------------"
for x in output:
	if "250" in x:
		print x

if (args.output is not None):
	with open(args.output,"w") as f:
		for x in output:
			if "250" in x:		
				f.write(x)
				f.write('\n')
print "created by Saint"
