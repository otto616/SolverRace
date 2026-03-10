import sys, os, random

# data structure to store the CNF
class CNF:
    def __init__(self):
        self.variables = 0
        self.num_clauses = 0
        self.clauses = []


def parse_input(cnf_file):   
    cnf = CNF()
    with open(cnf_file, 'r') as f:
        add_clause = cnf.clauses.append
        for line in f:

            # skip comments
            if line.startswith('c'):
                continue

            # parse the header
            if line.startswith('p'):
                parts = line.split()
                cnf.variables = int(parts[2])
                cnf.num_clauses = int(parts[3])
                continue

            parts = line.split()

            # skip empty lines
            if not parts:
                continue

            # parse the clauses with variables
            add_clause(list(map(int, parts[:-1])))
                
    return cnf


class Solver:
    def __init__(self, cnf):
        self.cnf = cnf
    
