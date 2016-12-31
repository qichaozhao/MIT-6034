from classify import *

##
## CSP portion of lab 4.
##
from csp import basic_constraint_checker
#
#
# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    cur_var = state.get_current_variable()

    if cur_var is not None:
        cur_var_value = cur_var.get_assigned_value()
        cur_var_constraints = state.get_constraints_by_name(cur_var.get_name())

        for c in cur_var_constraints:
            Y = state.get_variable_by_name(c.get_variable_j_name() if c.get_variable_j_name() != cur_var.get_name() else c.get_variable_i_name())

            if Y.is_assigned() is False:
                Y_domain = Y.get_domain()

                # print Y_domain

                for y in Y_domain:
                    constraint_check = c.check(state, value_i=cur_var_value, value_j=y)

                    if constraint_check is False:
                        Y.reduce_domain(y)

                if Y.domain_size() == 0:
                    return False

        return True

    else:
        return True


# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    # Get all domain_size = 1 vars.
    all_var = state.get_all_variables()
    singletons = set()
    visited_singletons = set()

    for var in all_var:
        if var.domain_size() == 1 and var.is_assigned() is False:
            singletons.update([var])

    if len(singletons) == 0:
        return True

    # keep looping unless we break
    while 1 == 1:

        # print singletons
        X = singletons.pop()
        visited_singletons.update([X])

        # print X._domain[0]
        # print X.get_assigned_value()

        X_val = X._domain[0]
        X_constraints = state.get_constraints_by_name(X.get_name())

        for c in X_constraints:

            Y = state.get_variable_by_name(c.get_variable_j_name() if c.get_variable_j_name() != X.get_name() else c.get_variable_i_name())

            if Y.is_assigned() is False:
                Y_domain = Y.get_domain()

                # print Y_domain

                for y in Y_domain:
                    constraint_check = c.check(state, value_i=X_val, value_j=y)

                    if constraint_check is False:
                        Y.reduce_domain(y)

            if Y.domain_size() == 1 and Y not in visited_singletons and Y not in singletons:
                singletons.update([Y])
            elif Y.domain_size() == 0:
                return False
            else:
                pass

        # print "Len singleton: " + str(len(singletons))
        if len(singletons) == 0:
            return True


## The code here are for the tester
## Do not change.

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)


##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')

### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)


# evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!

    squared_sum = 0
    for l1, l2 in zip(list1, list2):
        squared_sum += (l1 - l2) ** 2

    eucl_dist = squared_sum ** 0.5
    return eucl_dist


# Once you have implemented euclidean_distance, you can check the results:
# evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2, verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)

# evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
# print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    def get_disorder(list):
        import math

        # get a set of unique classes
        classes = set(list)
        branch_samples = float(len(list))

        disorder = 0
        for c in classes:
            disorder += -1 * ( list.count(c) / branch_samples ) * math.log( (list.count(c) / branch_samples), 2 )

        return disorder

    total_samples = float(len(yes) + len(no))
    avg_disorder = len(yes) / total_samples * get_disorder(yes) + len(no) / total_samples * get_disorder(no)

    return avg_disorder


# print CongressIDTree(senate_people, senate_votes, information_disorder)
# evaluate(idtree_maker(senate_votes, information_disorder), senate_group1, senate_group2, verbose=1)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose=False):
    house_limited, house_limited_votes = limit_votes(house_people,
                                                     house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1, verbose=False)
# print "Representatives classified correctly: " + str(rep_classified)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2, verbose=False)
# print "Senator classified correctly: " + str(senator_classified)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3, verbose=False)
# print "Old senator classified correctly: " + str(old_senator_classified)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "12"
WHAT_I_FOUND_INTERESTING = "Constraint Satisfaction"
WHAT_I_FOUND_BORING = "Not given the chance to program the KNN algo itself!"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose=0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in ['my_classifier']:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn