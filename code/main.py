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

def read_logical_file(file_name):
	#comment_line = re.compile('c.*')
	#stats_line = re.compile('p\s*cnf\s*(\d*)\s*(\d*)')
	#implication_line = re.compile(
	equivalence_line = 
	sentences = []
	with open(file_name, 'r') as fdata:
		for line in fdata:
			line = line.strip()
			if line:
				if implication_line.match(line):
					print line
				#nums = line.strip().split()
				#if nums:
					#nums.pop()
					#sentences.append(map(int, nums))
	return sentences

def main():
	if len(sys.argv) < 3:
		print "missing input file"
		print "USAGE: python main.py <base.txt> <new.txt>"
		exit()
	
	read_logical_file(sys.argv[1])
	
	#sentences = read_dimacs(sys.argv[1])
	#new_info = read_dimacs(sys.argv[2])
	
	#print "initial base:\n{}".format(sentences)
	#if is_inconsistent(sentences):
		#raise ValueError("original base is inconsistent")
	#print "new information:\n{}".format(new_info)
	#if is_inconsistent(new_info):
		#raise ValueError("new information is inconsistent")
	
	#revised_list = revision(sentences, new_info)
	#for i, revised in enumerate(revised_list):
		#print "revised base #{}:\n{}".format(i+1, revised)
		#if is_inconsistent(revised):
			#raise ValueError("revised base is inconsistent")
	
main()
