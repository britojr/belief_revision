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
	
	write_cnf("cnf_base3.txt", sentences)
	write_cnf("cnf_new3.txt", new_info)
	write_cnf("cnf_result3.txt", revised)

main()
