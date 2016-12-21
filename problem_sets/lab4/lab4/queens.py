#!/usr/bin/env python
"""
Implementation of the 9 by 9 sudoku problem
By: Justin Cullen for 6.034 Fall 2010
Date: Thursday, November 4th
"""
from csp import CSP, Variable, BinaryConstraint, solve_csp_problem

# initialise empty board.
# each element represents a column, the number of each element will represent the row the queen sits on
grid = [0,0,0,0,0,0,0,0]

def queen_problem(partial_grid=grid, num_queens=8):
    if len(partial_grid) <> num_queens: 'Error: Board dimensions be ' + str(num_queens)

    # Initialize...
    constraints = []
    indices = [i for i in range(0, 8)]
    variables = []

    # Initialize variables with one variable for each square.
    for i in indices:
        theval = [j for j in range(1,9)]

        variables.append(Variable(str(i), theval))

    # print len(variables)

    # returns the column of the queen
    def col(var):
        return int(var.get_name())

    # returns the row of the queen
    def row(var):
        try:
            return int(var.get_assigned_value())
        except TypeError:
            return 0

    # def is_on_same_diagonal(q1,q2):
    #     # Check if two queens lie on the same diagonal
    #     q1_col = col(q1)
    #     q1_row = row(q1)
    #
    #     q2_col = col(q2)
    #     q2_row = row(q2)
    #
    #     # Top left is 0,0
    #     # If two queens are on this diagonal: \ then x1 - x2 = y1 - y2
    #
    #     diag = False
    #     if q1_col - q2_col == q1_row - q2_row:
    #         diag = True
    #
    #     # If two queens are on this diagonal: / then x1 - x2 = y2 - y1
    #     if q1_col - q2_col == q2_row - q1_row:
    #         diag = True
    #
    #     return diag
    #
    # def is_on_same_row(q1,q2):
    #     return row(q1) == row(q2)

    # Note we don't actually need a is_same_col function because we already enforced this in our problem setup
    # def is_on_same_column(q1,q2):
    #     return col(q1) == col(q2)

    # if queen, not allowed to be on same row, column or diagonal
    def nomatch_constraint(val_a, val_b, name_a, name_b):
        if val_a == val_b:
            # same row
            return False

        if (int(name_a) - int(name_b) == val_a - val_b) or (int(name_a) - int(name_b) == val_b - val_a):
            # same diagonal
            return False

        return True

    edges = []
    for v1 in variables:
        for v2 in variables:
            if v1 != v2:
                edges.append((v1.get_name(), v2.get_name()))


    for e in edges:
        constraints.append(
            BinaryConstraint(e[0], e[1],
                             nomatch_constraint,
                             "Cant place queens on same row or diagonal!"))

    return CSP(constraints, variables)


# Outputs the solution given by the CSP in terms of an easily readible text form
def make_solution_readable(solution):
    solstate = solution[0]
    variables = [(v.get_name(), v.get_assigned_value()) for v in solstate.get_all_variables()]
    output = []
    for i in range(8):
        output.append([0, 0, 0, 0, 0, 0, 0, 0])
    for (name, val) in variables:
        i = int(name)
        j = val
        output[i][j - 1] = 1

    return output


if __name__ == "__main__":

    import lab4

    checker = lab4.forward_checking_prop_singleton


    sol = solve_csp_problem(queen_problem, checker, verbose=True)
    for row in make_solution_readable(sol):
        print row
