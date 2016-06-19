#!/usr/bin/python
import sys
from belief_change import *

#=============================
#main
#=============================
	
def print_base(expression):
	lines = expr_to_str(expression).split('&')
	for line in lines:
		print line.strip()
	print

def main():
	if len(sys.argv) < 3:
		print "missing input file"
		print "USAGE: python main.py <base.txt> <new.txt>"
		exit()
	
	knowledge_base = read_logical_file(sys.argv[1])
	revision_sentence = read_logical_file(sys.argv[2])
	
	#print "initial base:"
	#print_base(knowledge_base)
	if is_inconsistent(knowledge_base):
		raise ValueError("original base is inconsistent")
	#print "new information:"
	#print_base(revision_sentence)
	if is_inconsistent(revision_sentence):
		raise ValueError("new information is inconsistent")
	
	revised_list = revision(knowledge_base, revision_sentence)
	for i, revised in enumerate(revised_list):
		#print "revised base #{}:".format(i+1)
		#print_base(revised)
		if is_inconsistent(revised):
			raise ValueError("revised base is inconsistent")
	
main()
