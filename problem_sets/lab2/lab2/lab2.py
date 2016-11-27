# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
# ANSWER1 = True
# ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False


# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]

    # whilst we haven't found a valid path and the agenda is not empty
    while valid_path is False and len(agenda) > 0:
        # print path_memo
        # print agenda

        # Get the first item in the agenda
        node = agenda.pop(0)
        cur_path = path_memo.pop(0)

        if node == goal:
            # Great, the node is the goal, so let's return the cur_path
            path = cur_path
            valid_path = True

        else:
            # The node isn't the goal, so extend it and append the nodes to the back of the queue
            new_nodes = graph.get_connected_nodes(node)
            # print new_nodes
            # print cur_path
            for node in new_nodes:
                if node not in cur_path:
                    # We only want to append nodes that are not in the current path to avoid going in circles

                    agenda.append(node)
                    path_memo.append(cur_path + [node])
                    # print agenda
                    # print path_memo

    if valid_path is False:
        return []
    else:
        return path


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]

    # whilst we haven't found a valid path and the agenda is not empty
    while valid_path is False and len(agenda) > 0:
        # print path_memo
        # print agenda

        # Get the first item in the agenda
        node = agenda.pop(0)
        cur_path = path_memo.pop(0)

        if node == goal:
            # Great, the node is the goal, so let's return the cur_path
            path = cur_path
            valid_path = True

        else:
            # The node isn't the goal, so extend it and prepend the nodes to the front of the queue!
            new_nodes = graph.get_connected_nodes(node)
            # print new_nodes
            # print cur_path
            for node in new_nodes:
                if node not in cur_path:
                    # We only want to append nodes that are not in the current path to avoid going in circles

                    agenda.insert(0, node)
                    path_memo.insert(0, cur_path + [node])
                    # print agenda
                    # print path_memo

    if valid_path is False:
        return []
    else:
        return path


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False

    # now we need to initialise the agenda with the shortest path length first.
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]
    path_val = [graph.get_heuristic(x[1], goal) for x in path_memo]

    sorted_agenda = [a for (pv, a) in sorted(zip(path_val, agenda), key=lambda pair: pair[0])]
    sorted_path_memo = [pm for (pv, pm) in sorted(zip(path_val, path_memo), key=lambda pair: pair[0])]

    # whilst we haven't found a valid path and the agenda is not empty
    while valid_path is False and len(sorted_agenda) > 0:

        # print sorted_path_memo
        # print sorted_agenda

        # Get the first item in the agenda
        node = sorted_agenda.pop(0)
        cur_path = sorted_path_memo.pop(0)

        if node == goal:
            # Great, the node is the goal, so let's return the cur_path
            path = cur_path
            valid_path = True

        else:
            # The node isn't the goal, so extend it and prepend the nodes to the front of the queue!
            new_nodes = graph.get_connected_nodes(node)
            # print new_nodes
            # print cur_path
            # sort nodes by their distance to goal (so we are hillclimbing).
            new_path_val = [graph.get_heuristic(node, goal) for node in new_nodes]
            sorted_new_nodes = [n for (pv, n) in sorted(zip(new_path_val, new_nodes), key=lambda pair: pair[0])]

            # print new_path_val

            for node in sorted_new_nodes[::-1]:
                if node not in cur_path:
                    # We only want to append nodes that are not in the current path to avoid going in circles
                    sorted_agenda.insert(0, node)
                    sorted_path_memo.insert(0, cur_path + [node])
                    # print sorted_agenda
                    # print sorted_path_memo

    if valid_path is False:
        return []
    else:
        return path


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]

    # Before we start, we want to sort our agenda by our heuristic, and keep the best W where W is beam_width
    path_val = [graph.get_heuristic(node, goal) for node in agenda]
    sorted_agenda = [a for (pv, a) in sorted(zip(path_val, agenda), key=lambda pair: pair[0])]
    sorted_path_memo = [pm for (pv, pm) in sorted(zip(path_val, path_memo), key=lambda pair: pair[0])]

    if len(sorted_agenda) >= beam_width:
        sorted_agenda = sorted_agenda[0:beam_width]
        sorted_path_memo = sorted_path_memo[0:beam_width]

    new_agenda = []
    new_path_memo = []

    # whilst we haven't found a valid path and the agenda is not empty
    while valid_path is False:

        # Get the first item in the agenda
        try:
            node = sorted_agenda.pop(0)
            cur_path = sorted_path_memo.pop(0)
        except:
            # the list is now empty so we've reached the end of the level, time to populate the new level and continue
            agenda = new_agenda
            path_memo = new_path_memo

            # print agenda
            # print path_memo

            # Before we start, we want to sort our agenda by our heuristic, and keep the best W where W is beam_width
            path_val = [graph.get_heuristic(node, goal) for node in agenda]
            sorted_agenda = [a for (pv, a) in sorted(zip(path_val, agenda), key=lambda pair: pair[0])]
            sorted_path_memo = [pm for (pv, pm) in sorted(zip(path_val, path_memo), key=lambda pair: pair[0])]

            if len(sorted_agenda) >= beam_width:
                sorted_agenda = sorted_agenda[0:beam_width]
                sorted_path_memo = sorted_path_memo[0:beam_width]

            # print sorted_agenda
            # print sorted_path_memo

            # Now reset the levels
            new_agenda = []
            new_path_memo = []

            # Continue the algo
            try:
                node = sorted_agenda.pop(0)
                cur_path = sorted_path_memo.pop(0)
            except:
                # Now we really don't have any nodes left
                break

        # print sorted_agenda
        # print sorted_path_memo

        if node == goal:
            # Great, the node is the goal, so let's return the cur_path
            path = cur_path
            valid_path = True

        else:
            # The node isn't the goal, so extend it and append the nodes to the back of the queue
            new_nodes = graph.get_connected_nodes(node)
            for node in new_nodes:
                if node not in cur_path:
                    new_agenda.append(node)
                    new_path_memo.append(cur_path + [node])

    if valid_path is False:
        return []
    else:
        return path


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    path = 0
    for i in range(0, len(node_names) - 1):
        path = path + graph.get_edge(node_names[i], node_names[i + 1]).length

    return path


def branch_and_bound(graph, start, goal):
    # Branch and bound attempts to extend the shortest path on every pass

    # print "start = " + start
    # print "goal = " + goal

    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]
    path_vals = [path_length(graph, x) for x in path_memo]

    while valid_path == False and len(agenda) > 0:

        # pick the shortest path
        idx_min = path_vals.index(min(path_vals))

        # set our current variables to the shortest path
        node = agenda.pop(idx_min)
        cur_path = path_memo.pop(idx_min)
        cur_path_len = path_vals.pop(idx_min)

        # print node
        # print cur_path
        # print cur_path_len

        # print path_vals
        if node == goal:

            path = cur_path
            valid_path = True

        else:

            # extend this path
            new_nodes = graph.get_connected_nodes(node)
            for node in new_nodes:
                if node not in cur_path:
                    # We only want to append nodes that are not in the current path to avoid going in circles
                    agenda.insert(0, node)
                    path_memo.insert(0, cur_path + [node])
                    path_vals.insert(0, path_length(graph, cur_path + [node]))

    if valid_path is False:
        return []
    else:
        return path


def a_star(graph, start, goal):
    # A* is branch and bound with extended set list + directional heuristic

    if start == goal:
        # account for the trivial case
        return [goal]

    path = []
    valid_path = False
    agenda = (graph.get_connected_nodes(start))
    path_memo = [[start, x] for x in agenda]
    path_lens = [path_length(graph, x) for x in path_memo]
    path_heu = [graph.get_heuristic(node, goal) for node in agenda]

    path_values = [l + h for l, h in zip(path_lens, path_heu)]

    extended = set([])

    while valid_path == False and len(agenda) > 0:

        # pick the shortest path based on the heuristic + the path length
        idx_min = path_values.index(min(path_values))

        # set our current variables to the shortest path
        node = agenda.pop(idx_min)
        cur_path = path_memo.pop(idx_min)
        cur_path_heu = path_values.pop(idx_min)

        # print node
        # print cur_path
        # print cur_path_heu

        # print path_vals
        if node == goal:

            path = cur_path
            valid_path = True

        else:

            # add this to our set of extended nodes
            extended.add(node)

            # extend this path
            new_nodes = graph.get_connected_nodes(node)

            for node in new_nodes:
                if node not in cur_path and node not in extended:
                    # We only want to append nodes that are not in the current path to avoid going in circles nor extended already to save time
                    agenda.insert(0, node)
                    path_memo.insert(0, cur_path + [node])
                    path_values.insert(0, path_length(graph, cur_path + [node]) + graph.get_heuristic(node, goal))

    if valid_path is False:
        return []
    else:
        return path


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    # Let's use standard DFS as our gold standard to measure the heuristic against :D
    # Admissability is defined as if the heuristic estimate of a node to the goal is less than the true cost of the node to the goal (i.e. the estimate of distance is never over the true value)

    graph_nodes = graph.nodes
    for node in graph_nodes:
        dfs_path = dfs(graph, node, goal)
        dfs_length = path_length(graph, dfs_path)

        # print dfs_path
        # print dfs_length


        heuristic = graph.get_heuristic(node, goal)

        # print heuristic

        if heuristic > dfs_length:
            return False

    return True


def is_consistent(graph, goal):
    # Consitency is defined as when the heuristic estimate of a neighbour node to the goal + the true distance from the current node to the neighbour is less than or equal to the estimated cost from
    # the current node to the goal.

    # print "Goal is: " + goal
    graph_nodes = graph.nodes
    for node in graph_nodes:

        # print "Currently tested node is: " + node
        node_heuristic = graph.get_heuristic(node, goal)
        # print "Heuristic for node is: " + str(node_heuristic)

        neighbours = graph.get_connected_nodes(node)
        for n in neighbours:
            # print "Currently tested neighbour is: " + n
            neighbour_distance = graph.get_edge(node, n).length
            neighbour_heuristic = graph.get_heuristic(n, goal)

            # print "Neighbour distance is: " + str(neighbour_distance)
            # print "Neighbour heuristic is: " + str(neighbour_heuristic)

            if (neighbour_distance + neighbour_heuristic) < node_heuristic:
                return False

    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '7'
WHAT_I_FOUND_INTERESTING = 'EVERYTHING'
WHAT_I_FOUND_BORING = 'NOTHING'
