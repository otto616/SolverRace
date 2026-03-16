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
        self.assignment = [] 
        self.var_to_clause = [] 
        self.true_lit_count = [] 
        self.unsatisfied = set() 

    def initialize_state(self):

        # variable which stores the assignments True (1) or False (0) of each variable
        self.assignment = [None] + [random.getrandbits(1) for _ in range(self.cnf.variables)]
        # In here we store where each variable appears
        self.var_to_clause = [[] for _ in range(self.cnf.variables + 1)]
        self.true_lit_count = [0] * self.cnf.num_clauses
        self.unsatisfied = set()

        # Iterate all the clauses one time
        for clause_index, clause in enumerate(self.cnf.clauses):
            true_lits = 0
            
            # Iterate current clausE
            for lit in clause:
                var = abs(lit)
                
                # Add index of the clause in which appears that variable
                # If later we need to change variables true/false, we don't want to iterate all again to know where some variable is
                self.var_to_clause[var].append((clause_index, lit))

                # Check if literal satisfies the clause with the current rand. assignation
                # Assignments is full of 0s and 1s so if a literal is positive and it is assigned to positive (1) it will satisfy
                if (lit > 0) == self.assignment[var]:
                    true_lits += 1

            # Once we iterated all the clause, we store how many literals in it are true
            self.true_lit_count[clause_index] = true_lits

            # If no literal is true, the clause is unsat
            if true_lits == 0:
                self.unsatisfied.add(clause_index)


    # This function calculates how many clauses are one flip away from being unsat, by the given variable
    def calculate_break_count(self, var):
        breaks = 0
        var_value = self.assignment[var]
        # For each clause where this var appears, we search for how many will we unsat if we flip it's value
        # We ignore if we repair any clause with the flip (walksat strategy)
        for i, literal in self.var_to_clause[var]:
            if self.true_lit_count[i] == 1:
                if (literal > 0) == var_value:
                    breaks += 1
        
        return breaks
        
        
        # inefficient version
        for i in self.var_to_clause[var]:

            if self.true_lit_count[i] == 1:

                test_clause = self.cnf.clauses[i]

                for lit in test_clause:
                    if var == abs(lit):
                        if (lit > 0) == self.assignment[var]:
                            breaks += 1
                            break # A var only appears once in a clause

        return breaks
            

    def pick_variable_to_flip(self, clause_idx, walk_probability=0.5):

        clause = self.cnf.clauses[clause_idx]
        
        min_damage = float('inf')
        best_var = None
        
        for literal in clause:
            abs_var = abs(literal)
            damage = self.calculate_break_count(abs_var)
            
            # If there is a variable that won't break any clause, we select it
            if damage == 0:
                return abs_var
                
            # Else we store the variable which makes less "damage"
            if damage < min_damage:
                min_damage = damage
                best_var = abs_var
                
        # Random Walk 
        if random.random() < walk_probability:
            # If we have to do the random walk, we choose a random var from the current clause
            return abs(random.choice(clause))
            
        # Else we return the Greedy
        return best_var

        # Inefficient version
        breakings = {}

        for variable in self.cnf.clauses[clause_idx]:

            abs_var = abs(variable)
            damage = self.calculate_break_count(abs_var)

            if damage == 0:
                return abs_var
        
            else:
                breakings[abs_var] = damage
            
        if (random.random() < walk_probability):
            return random.choice(list(breakings.keys()))
                
        else:
            return min(breakings, key = breakings.get)



    def flip(self, var):
        """
        1. Inverteix el valor de self.assignment[var] (de 0 a 1 o d'1 a 0).
        2. Recorre self.var_to_clause[var] i actualitza el self.true_lit_count 
           de cada clàusula afectada.
        3. Si una clàusula passa a true_lit_count == 0, afegeix-la a self.unsatisfied.
        4. Si una clàusula passa de 0 a 1, treu-la de self.unsatisfied.
        """
        pass

    def solve(self, max_flips=100000, max_restarts=10):
        """
        El bucle principal de l'algorisme.
        Per 'max_restarts' vegades:
            Crida self.initialize_state()
            Per 'max_flips' vegades:
                Si len(self.unsatisfied) == 0:
                    Has trobat la solució! Retorna True.
                Agafa una clàusula aleatòria de self.unsatisfied.
                var = self.pick_variable_to_flip(clausula)
                self.flip(var)
        Si s'acaben els restarts i no hi ha solució, retorna False.
        """
        pass

def print_solution(assignment):
    """
    Imprimeix el resultat exactament com demana la pràctica:
    s SATISFIABLE
    v 1 -2 3 -4 ... 0
    (Recorda transformar els 0s i 1s de l'assignació en variables positives i negatives).
    """
    pass

if __name__ == '__main__':
    # 1. Comprovar que ens passen el fitxer per arguments (sys.argv)
    if len(sys.argv) != 2:
        print("c Ús: python3 solver.py <arxiu.cnf>")
        sys.exit(1)
        
    cnf_file = sys.argv[1]
    
    # 2. Parsejar
    cnf = parse_input(cnf_file)
    
    # 3. Instanciar i resoldre
    solver = Solver(cnf)
    found_solution = solver.solve(max_flips=100000, max_restarts=50)
    
    # 4. Imprimir
    if found_solution:
        print_solution(solver.assignment)
    else:
        # Pels requeriments, si no troba solució no fa falta imprimir res especial,
        # però pots posar un missatge de comentari per debug.
        print("c Timeout o solució no trobada")
    
