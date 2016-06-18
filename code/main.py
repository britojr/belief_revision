#!/usr/bin/python
import sys
from belief_revision import *

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
	
	sentences = read_dimacs(sys.argv[1])
	new_info = read_dimacs(sys.argv[2])
	
	print "initial base:\n{}".format(sentences)
	if is_inconsistent(sentences):
		raise ValueError("original base is inconsistent")
	print "new information:\n{}".format(new_info)
	if is_inconsistent(new_info):
		raise ValueError("new information is inconsistent")
	
	revised_list = revision(sentences, new_info)
	for i, revised in enumerate(revised_list):
		print "revised base #{}:\n{}".format(i+1, revised)
		if is_inconsistent(revised):
			raise ValueError("revised base is inconsistent")
	
main()
