from sympy import symbols, Not, Or, And, Implies, Equivalent, to_cnf, to_dnf
#Kevin Ruiz - 3/1/2024

def task_1():
    A = True
    B = False

    # (1) not A
    result_1 = not A

    # (2) A or B
    result_2 = A or B

    # (3) A and B
    result_3 = A and B

    # (4) A implies B
    result_4 = Implies(A, B)

    # (5) B implies A
    result_5 = Implies(B, A)

    # (6) A <-> B (Biconditional)
    result_6 = Equivalent(A, B)

    return result_1, result_2, result_3, result_4, result_5, result_6

def task_2(expression):
    # Convert to CNF
    cnf_expression = to_cnf(expression)

    # Convert to DNF
    dnf_expression = to_dnf(expression)

    return cnf_expression, dnf_expression

if __name__ == "__main__":
    # Task 1
    results_task_1 = task_1()
    print("Results of Task 1:")
    print("(1) not A:", results_task_1[0])
    print("(2) A or B:", results_task_1[1])
    print("(3) A and B:", results_task_1[2])
    print("(4) A implies B:", results_task_1[3])
    print("(5) B implies A:", results_task_1[4])
    print("(6) A <-> B (Biconditional):", results_task_1[5])

    # Task 2
    expression = symbols('C') | Not((symbols('A') | symbols('B')))
    cnf_expression, dnf_expression = task_2(expression)
    print("\nResults of Task 2:")
    print("Original Expression:", expression)
    print("CNF:", cnf_expression)
    print("DNF:", dnf_expression)