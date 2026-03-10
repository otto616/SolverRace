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
        cnf = CNF()

        self.assignment = [None] + [random.getrandbits(1) for _ in range(self.cnf.variables)]
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
                self.var_to_clause[var].append(clause_index)

                # Check if literal satisfies the clause with the current rand. assignation
                # Assignments is full of 0s and 1s so if a literal is positive and it is assigned to positive (1) it will satisfy
                if (lit > 0) == self.assignment[var]:
                    true_lits += 1

            # Once we iterated all the clause, we store how many literals in it are true
            self.true_lit_count[clause_index] = true_lits

            # If no literal is true, the clause is unsat
            if true_lits == 0:
                self.unsatisfied.add(clause_index)



    def calculate_break_count(self, var):
        """
        Calcula quantes clàusules que ARA MATEIX estan satisfetes 
        es trencarien si canviem el valor d'aquesta 'var'.
        (Pista: Només has de mirar les clàusules a self.var_to_clause[var] 
        que tinguin self.true_lit_count == 1 i on la 'var' sigui la que ho fa cert).
        Retorna un número enter.
        """
        breaks = 0

        for i self.var_to_clause[var]:

            if self.true_lit_count[i] == 0:
                # Flipping it will make it true necessarily
                breaks -= 1 

            if self.true_lit_count[i] == 1:

                test_clause = cnf.clauses[i]

                for lit in test_clause:

                    if var == abs(lit):
                        if (lit > 0) == self.assignment[var]:
                            breaks += 1
            

                    

    def pick_variable_to_flip(self, clause_idx, walk_probability=0.5):
        """
        Lògica de WalkSAT per escollir quina variable canviar dins d'una clàusula trencada:
        1. Mira les variables de la clàusula a l'índex 'clause_idx'.
        2. Si alguna variable té un break_count == 0, escull-la immediatament.
        3. Si no, amb probabilitat 'walk_probability', escull una variable a l'atzar.
        4. Si no, escull la variable que tingui el break_count més baix.
        Retorna l'índex (enter) de la variable escollida.
        """
        pass

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
    
