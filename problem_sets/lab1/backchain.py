from production import AND, OR, match, populate, simplify, RuleExpression
from zookeeper import ZOOKEEPER_RULES


# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    """
    backchaining
    :param rules:
    :param hypothesis:
    :return:
    """

    # the result at its base has to be the hypothesis
    result = [hypothesis]

    # loop through rules
    for r in rules:

        # get the consequent of the rule
        con = r.consequent()

        # loop through the consequents
        for c in con:

            # see if we can bind
            tmp_bind = match(c, hypothesis)

            if tmp_bind is not None:

                # Now we have to get the antecedents
                ant = r.antecedent()

                if isinstance(ant, RuleExpression):
                    # now we have to loop through the antecedents and do some recursion
                    if isinstance(ant, AND):
                        new_result = AND([backchain_to_goal_tree(rules, populate(expr, tmp_bind)) for expr in ant])

                    else:
                        new_result = OR([backchain_to_goal_tree(rules, populate(expr, tmp_bind)) for expr in ant])

                    result.append(new_result)

                else:
                    # so we know the antecedent is just a string (so we are at a leaf)
                    new_hypothesis = populate(ant, tmp_bind)
                    result.append(OR(backchain_to_goal_tree(rules, new_hypothesis)))

    return simplify(OR(result))


# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
