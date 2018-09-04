import argparse
import getpass
import sys
import telnetlib
import os.path

parser=argparse.ArgumentParser(description='Verify usernames through SMTP RCPT commands')
parser.add_argument('hosts', nargs='+',
 help="specify target host address (or addresses)")
parser.add_argument('-p', nargs='?', type=int, default=25,
help="specify port (default is 25)", dest="port")
parser.add_argument('-U', help="list of possible usernames", dest="users_file")
parser.add_argument('-v', help="enable verbosity",
 action="store_true", dest="verbose")
parser.add_argument('-o', help="output file", dest="output")

args=parser.parse_args()
#Check arguments
if ((args.hosts is None) or (args.users_file is None)): 
	print "Error, use the -h help to learn more about this script"
	parser.print_help()
	sys.exit(1)
if (os.path.isfile(args.users_file) == False):
	print "Username list at " + args.users_file + " path is incorrect please double check"
	sys.exit(1)

users_file=args.users_file
port=args.port
hosts=[]
#Check to see if we have 1 or more hosts
if (isinstance(args.hosts,str)):
	hosts.append(args.hosts)
elif (isinstance(args.hosts,list)):
	hosts=args.hosts
#Telnet in using the arguments
#Range is hosts
outputa=[]
for host in hosts:
	
	tn = telnetlib.Telnet(host,port)
	tn.write("helo x" + "\n")
	tn.write("mail from: roguer@slax.example.net" + "\n")
	 
	#we wait for the Sender ok command
	print "SMTP username verification on " + host + " is in progress please wait.."
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
		outputa.append(temp)
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
