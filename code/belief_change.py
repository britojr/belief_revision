#!/usr/bin/python
import itertools
import copy
from sympy import symbols
from sympy.logic.boolalg import to_cnf, And, Equivalent, Not
from sympy.logic.inference import satisfiable
from sympy.printing.pretty.pretty import PrettyPrinter

#read file and returns a cnf expression
def read_logical_file(file_name):
	with open(file_name, 'r') as fdata:
		cnf_expression = reduce(And, map(to_cnf, [line.strip() for line in fdata if line.strip()]))
	return cnf_expression

#convert an expression to a string, replacing non ASCII characteres
def expr_to_str(expression):
	decode_symbols = {
		u'\xac'		: '~',
		u'\u2227'	: '&',
		u'\u2228'	: '|'
	}
	print_settings = {
		"order": None,
		"full_prec": "auto",
		"use_unicode": None,
		"wrap_line": True,
		"num_columns": 5000,
		"use_unicode_sqrt_char": True,
	}
	s = PrettyPrinter(settings=print_settings).doprint(expression)
	for symb, dec_symb in decode_symbols.iteritems():
		s = s.replace(symb, dec_symb)
	return s

def expr_concat(*expressions):
	return reduce(And, expressions)

#returns the list of atoms of a given expression
def get_atoms(expression):
	return expression.atoms()

#replace the old atom value for the new atom value in the expression	
def replace(expression, old, new):
	return expression.subs(old, new)

def is_inconsistent(expression):
	return not satisfiable(expression)

def primed(atom):
	return symbols(str(atom)+"_pr")

#change the atoms in the given expression by the prime value p
def prime(expression, atoms):
	primed_expression = copy.deepcopy(expression)
	for atom in atoms:
		primed_expression = replace(primed_expression, atom, primed(atom))
	return primed_expression

def equivalence(a, b):
	return to_cnf(Equivalent(a, b))

#returns the equivalence clauses for each atom and its respective prime value
def get_equivalence_clauses(atoms):
	return reduce(And, [equivalence(a, primed(a)) for a in atoms])
	#return expr_concat([equivalence(a, primed(a)) for a in atoms])

#returns a list of the maximal equivalence sets
def get_max_equivalence_sets(union_base, conflict_atoms):
	minimal_inconsistent_sets = []
	maximal_consistent_sets = []
	
	#iterate through the possible combinations of atoms, descending on size
	#for set_size in reversed(xrange(len(conflict_atoms), 0, -1)):
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
			if is_inconsistent(expr_concat(union_base, get_equivalence_clauses(atoms_set))):
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
	primed_base = prime(knowlege_base, conflict_atoms)
	
	union_base = expr_concat(primed_base, revision_clauses)
	maximal_consistent_sets = get_max_equivalence_sets(union_base, conflict_atoms)
	
	revised_base_list = []
	for equivalence_set in maximal_consistent_sets:
		revised_base_list.append(copy.deepcopy(union_base))
		for atom in conflict_atoms:
			if atom in equivalence_set:
				revised_base_list[-1] = replace(revised_base_list[-1], primed(atom), atom)
			else:
				revised_base_list[-1] = replace(revised_base_list[-1], primed(atom), Not(atom))
	return revised_base_list
