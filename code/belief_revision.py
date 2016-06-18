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

def revision(knowlege_base, revision_clauses):
	if inconsistent(knowlege_base) or inconsistent(revision_clauses):		return None
	atom_in = []
	atom_out = []
	cflict_atoms = get_atoms(knowlege_base).intersection(get_atoms(revision_clauses))
	prime_value = max(max(get_atoms(knowlege_base)), max(get_atoms(revision_clauses)))
	revised_base = prime(knowlege_base, cflict_atoms, prime_value)
	union_base = []
	union_base.extend(revised_base)
	union_base.extend(revision_clauses)
	for a in cflict_atoms:
		#equivalence: a <-> a+p => [[-a, a+p], [a, -a-p]]
		union_base.extend( [[-a, a+prime_value], [a, -a-prime_value]] )
		if inconsistent(union_base):
			atom_out.append(a)
			del union_base[-2:]
		else:
			atom_in.append(a)
	for a in atom_in:
		replace(revised_base, a+prime_value, a)
	for a in atom_out:
		replace(revised_base, a+prime_value, -a)
	revised_base.extend(revision_clauses)
	return revised_base

