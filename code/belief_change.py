#!/usr/bin/python
import pycosat
import itertools
import copy
import re

#read a file in DIMACS format and returns a list of sentences
def read_dimacs(file_name):
	comment_line = re.compile('c.*')
	stats_line = re.compile('p\s*cnf\s*(\d*)\s*(\d*)')
	sentences = []
	with open(file_name, 'r') as fdata:
		for line in fdata:
			line = line.strip()
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

def is_inconsistent(sentences):
	return pycosat.solve(sentences) == "UNSAT"

#equivalence: a <=> b == [[a, -b], [-a, b]]
def equivalence(a, b):
	return [[a, -b], [-a, b]]

#returns a revised base
def simple_revision(knowlege_base, revision_clauses):
	if is_inconsistent(knowlege_base) or is_inconsistent(revision_clauses):		return None
	atom_in = []
	atom_out = []
	conflict_atoms = get_atoms(knowlege_base).intersection(get_atoms(revision_clauses))
	prime_value = max(max(get_atoms(knowlege_base)), max(get_atoms(revision_clauses)))
	revised_base = prime(knowlege_base, conflict_atoms, prime_value)
	union_base = revised_base + revision_clauses
	for a in conflict_atoms:
		union_base.extend(equivalence(a, a+prime_value))
		if is_inconsistent(union_base):
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

#returns the equivalence clauses for each atom and its respective prime value
def get_equivalence_clauses(atoms, prime_value):
	equivalences = []
	for a in atoms:
		equivalences.extend(equivalence(a, a+prime_value))
	return equivalences

#returns a list of the maximal equivalence sets
def get_max_equivalence_sets(union_base, conflict_atoms, prime_value):
	minimal_inconsistent_sets = []
	maximal_consistent_sets = []
	
	#iterate through the possible combinations of atoms, descending on size
	for set_size in xrange(len(conflict_atoms), 0, -1):
		comb_list = itertools.combinations(conflict_atoms, set_size)
		for comb in comb_list:
			atoms_set = set(comb)
			inconsist = False
			consist = False
			
			#skip this set if it is a superset of a minimal inconsistent set already known
			for inc_set in minimal_inconsistent_sets:
				if atoms_set.issuperset(inc_set):
					inconsist = True
					break
			if inconsist:	continue
			#skip this set if it is a subset of a maximal consistent set already known
			for cons_set in maximal_consistent_sets:
				if atoms_set.issubset(cons_set):
					consist = True
					break
			if consist:	continue
			
			#test if the formula (union_base and this set) is satisfiable
			if is_inconsistent(union_base + get_equivalence_clauses(atoms_set, prime_value)):
				#add a minimal inconsistent set and remove its supersets
				for inc_set in minimal_inconsistent_sets:
					if atoms_set.issubset(inc_set):
						minimal_inconsistent_sets.remove(inc_set)
				minimal_inconsistent_sets.append(atoms_set)
			else:
				#add a maximal consistent set and remove its subsets
				for cons_set in maximal_consistent_sets:
					if atoms_set.issuperset(cons_set):
						maximal_consistent_sets.remove(cons_set)
				maximal_consistent_sets.append(atoms_set)
			
	return maximal_consistent_sets

#returns a revised base for each maximal equivalence set
def revision(knowlege_base, revision_clauses):
	if is_inconsistent(knowlege_base) or is_inconsistent(revision_clauses):		return None
	conflict_atoms = get_atoms(knowlege_base).intersection(get_atoms(revision_clauses))
	prime_value = max(max(get_atoms(knowlege_base)), max(get_atoms(revision_clauses)))
	primed_base = prime(knowlege_base, conflict_atoms, prime_value)
	
	union_base = primed_base + revision_clauses
	maximal_consistent_sets = get_max_equivalence_sets(union_base, conflict_atoms, prime_value)
	
	revised_base_list = []
	for equivalence_set in maximal_consistent_sets:
		revised_base_list.append(copy.deepcopy(union_base))
		for atom in conflict_atoms:
			if atom in equivalence_set:
				replace(revised_base_list[-1], atom+prime_value, atom)
			else:
				replace(revised_base_list[-1], atom+prime_value, -atom)
	return revised_base_list
