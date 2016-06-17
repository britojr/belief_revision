#!/usr/bin/python
import sys
from belief_revision import *

#=============================
#main
#=============================

def main():
	if len(sys.argv) < 3:
		print "missing input file"
		print "USAGE: python main.py <base.txt> <new.txt>"
		exit()
	
	sentences = read_dimacs(sys.argv[1])
	print "initial base:\n{}".format(sentences)
	if inconsistent(sentences):
		raise ValueError("base is inconsistent")
	
	new_info = read_dimacs(sys.argv[2])
	print "new information:\n{}".format(new_info)
	if inconsistent(new_info):
		raise ValueError("new information is inconsistent")
	
	revised = belief_change(sentences, new_info, C=[])
	print "revised base:\n{}".format(revised)
	if inconsistent(revised):
		raise ValueError("revised base is inconsistent")
	
main()
