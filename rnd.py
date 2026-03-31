import os
import random  # Importar os para manejar directorios
import sys  # Importar sys para manejar argumentos de línea de comandos

class Clause:
    """A Clause in a CNF formula"""

    def __init__(self, num_vars, clause_length):
        """
        Initialization
        num_vars: Number of variables
        clause_length: Length of the clause
        lits: List of literals in the clause
        """
        self.lits = random.sample(range(1, num_vars + 1), clause_length)
        self.lits = [lit if random.choice([True, False]) else -lit for lit in self.lits]

class CNF():
    """A CNF formula randomly generated"""

    def __init__(self, num_vars, num_clauses, clause_length):
        """
        Initialization
        num_vars: Number of variables
        num_clauses: Number of clauses
        clause_length: Length of the clauses
        clauses: List of clauses
        """
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.clause_length = clause_length
        self.clauses = None
        self.gen_random_clauses()

    def gen_random_clauses(self):
        """Generate random clauses"""
        self.clauses = []
        for i in range(self.num_clauses):
            c = Clause(self.num_vars, self.clause_length)
            self.clauses.append(c)

    def save_to_file(self, filename):
        """Save the formula to a file"""
        with open(filename, "w") as f:
            f.write("c Random CNF formula\n")
            f.write("p cnf %d %d\n" % (self.num_vars, self.num_clauses))
            for c in self.clauses:
                f.write("%s 0\n" % " ".join(str(l) for l in c.lits))


# Main

if __name__ == '__main__':
    # A random CNF generator

    # Check parameters
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        sys.exit("Use: %s <num-vars> <num-clauses> <clause-length> [<random-seed>]" % sys.argv[0])

    try:
        num_vars = int(sys.argv[1])
    except:
        sys.exit("ERROR: Number of variables not an integer (%s)." % sys.argv[1])
    if num_vars < 1:
        sys.exit("ERROR: Number of variables must be >= 1 (%d)." % num_vars)

    try:
        num_clauses = int(sys.argv[2])
    except:
        sys.exit("ERROR: Number of clauses not an integer (%s)." % sys.argv[2])
    if num_vars < 1:
        sys.exit("ERROR: Number of clauses must be >= 1 (%d)." % num_clauses)

    try:
        clause_length = int(sys.argv[3])
    except:
        sys.exit("ERROR: Length of clauses not an integer (%s)." % sys.argv[3])
    if num_vars < 1:
        sys.exit("ERROR: Length of clauses must be >= 1 (%d)." % clause_length)

    if len(sys.argv) > 4:
        try:
            seed = int(sys.argv[4])
        except:
            sys.exit("ERROR: Seed number not an integer (%s)." % sys.argv[4])
    else:
        seed = None

    # Initialize random seed (current time)
    random.seed(seed)

    # Create the Benchmarks folder if it doesn't exist
    benchmarks_folder = "Benchmarks"
    if not os.path.exists(benchmarks_folder):
        os.makedirs(benchmarks_folder)

    # Generate the CNF formula
    cnf_formula = CNF(num_vars, num_clauses, clause_length)

    # Save the formula to a file
    filename = os.path.join(benchmarks_folder, f"cnf_{num_vars}_{num_clauses}_{clause_length}.cnf")
    cnf_formula.save_to_file(filename)

    print(f"CNF formula saved to {filename}")