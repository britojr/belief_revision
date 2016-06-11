#!/usr/bin/python
import sys
#from probmod import *
#import numpy as np
#from satispy import Variable, Cnf
#from satispy.solver import Minisat
#from sympy import *
import pycosat

#=============================
#main
#=============================
#read a file in DIMACS format and returns a list of sentences
def read_dimacs(file_name):
	sentences = []
	with open(file_name, 'r') as fdata:
		for line in fdata:
			aux = line.strip().split()
			if aux:
				if aux[0] == "p":
					num_var = int(aux[2])
				elif aux[0] not in ["c", "p"]:
					aux.pop()
					sentences.append(map(int, aux))
	return sentences, num_var

def get_atoms(sentences):
	return set([abs(a) for s in sentences for a in s])

def prime(sentences, atoms, p):
	t = []
	for s in sentences:
		q = []
		for a in s:
			if abs(a) in atoms:
				if a > 0: q.append(a+p)
				else: q.append(a-p)
			else:
				q.append(a)
		t.append(q)
	return t

def belief_change(K, R, C, p):
	if pycosat.solve(K) == "UNSAT" or pycosat.solve(R) == "UNSAT":
		return R
	atom_in = []
	atom_out = []
	#atoms = get_atoms(K).intersection(get_atoms(R).union(get_atoms(C)))
	atoms = get_atoms(K).union(get_atoms(R).union(get_atoms(C)))
	K_ = prime(K, atoms, p)
	aux = []
	aux.extend(K_)
	aux.extend(R)
	for a in reversed(sorted(list(atoms))):
		# a <-> a+p => [[-a, a+p], [a, -a-p]]
		#aux = [[-a, a+p], [a, -a-p]]
		#aux.extend( [[-x, x+p] for x in atom_in] )
		#aux.extend( [[x, -x-p] for x in atom_in] )
		aux.extend( [[-a, a+p], [a, -a-p]] )
		print a
		print aux
		if pycosat.solve(aux) == "UNSAT":
			atom_out.append(a)
			aux.pop()
			aux.pop()
		else:
			atom_in.append(a)
	for a in atom_in:
		replace(K_, a+p, a)
	for a in atom_out:
		replace(K_, a+p, -a)
	K_.extend(R)
	return K_
	
def replace(sentences, old, new):
	for s in sentences:
		for i in xrange(len(s)):
			if abs(s[i]) == old:
				if s[i] > 0: s[i] = new
				else: s[i] = -new

def main():
	if len(sys.argv) < 3:
		print "missing input file"
		print "USAGE: python main.py base.txt new.txt"
		exit()
	
	#read sentences in DIMACS file format
	sentences, a = read_dimacs(sys.argv[1])
	new_info, b = read_dimacs(sys.argv[2])
	num_var = max(a,b)
	
	revised = belief_change(sentences, new_info, [], num_var)
	print revised
	print pycosat.solve(revised)
	
main()
