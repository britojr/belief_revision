#!/usr/bin/python
import pycosat
import re

#read a file in DIMACS format and returns a list of sentences
def read_dimacs(file_name):
	comment_line = re.compile('c.*')
	stats_line = re.compile('p\s*cnf\s*(\d*)\s*(\d*)')
	sentences = []
	with open(file_name, 'r') as fdata:
		for line in fdata:
			if line and not comment_line.match(line) and not stats_line.match(line):
				nums = line.strip().split()
				if nums:
					nums.pop()
					sentences.append(map(int, nums))
	return sentences

#returns the list of atoms of a given sentence
def get_atoms(sentences):
	return set([abs(atom) for clause in sentences for atom in clause])

#change the atoms in the given sentences by the prime value p
def prime(sentences, atoms, prime_value):
	primed_sentences = []
	for clause in sentences:
		new_clause = []
		for atom in clause:
			if abs(atom) in atoms:
				if atom > 0:	new_clause.append(atom + prime_value)
				else:				new_clause.append(atom - prime_value)
			else:
				new_clause.append(atom)
		primed_sentences.append(new_clause)
	return primed_sentences

#replace the old atom value for the new atom value in the list of sentences	
def replace(sentences, old, new):
	for clause in sentences:
		for i in xrange(len(clause)):
			if abs(clause[i]) == old:
				if clause[i] > 0:	clause[i] = new
				else: 				clause[i] = -new

def inconsistent(sentences):
	return pycosat.solve(sentences) == "UNSAT"

def belief_change(K, R, C):
	if inconsistent(K) or inconsistent(R):		return None
	atom_in = []
	atom_out = []
	atoms = get_atoms(K).intersection(get_atoms(R).union(get_atoms(C)))
	prime_value = max(max(get_atoms(K)), max(get_atoms(R)))
	K_ = prime(K, atoms, prime_value)
	aux = []
	aux.extend(K_)
	aux.extend(R)
	for a in atoms:
		#equivalence: a <-> a+p => [[-a, a+p], [a, -a-p]]
		aux.extend( [[-a, a+prime_value], [a, -a-prime_value]] )
		if inconsistent(aux):
			atom_out.append(a)
			aux.pop()
			aux.pop()
		else:
			atom_in.append(a)
	for a in atom_in:
		replace(K_, a+prime_value, a)
	for a in atom_out:
		replace(K_, a+prime_value, -a)
	K_.extend(R)
	return K_

