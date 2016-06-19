#!/usr/bin/python
import sys
from belief_change import *

#=============================
#main
#=============================

def write_cnf(file_name, sentences):
	fout = open(file_name, "w")
	for clause in sentences:
		s="("
		signal=""
		for i, atom in enumerate(clause):
			if i: signal="+"
			if atom > 0:
				s+= "{}{}".format(signal, atom)
			else:
				s+= "{}~{}".format(signal, abs(atom))
		s+=")"
		fout.write(s + "\n")
	fout.close()

def main():
	if len(sys.argv) < 3:
		print "missing input file"
		print "USAGE: python main.py <base.txt> <new.txt>"
		exit()
	
	knowledge_base = read_logical_file(sys.argv[1])
	revision_sentence = read_logical_file(sys.argv[2])
	
	print "initial base:\n{}".format(expression_to_str(knowledge_base))
	if is_inconsistent(knowledge_base):
		raise ValueError("original base is inconsistent")
	print "new information:\n{}".format(revision_sentence)
	if is_inconsistent(revision_sentence):
		raise ValueError("new information is inconsistent")
	
	#revised_list = revision(sentences, new_info)
	#for i, revised in enumerate(revised_list):
		#print "revised base #{}:\n{}".format(i+1, revised)
		#if is_inconsistent(revised):
			#raise ValueError("revised base is inconsistent")
	
main()
