#!/usr/bin/env python
# 6.034 Lab 5
# Neural Net
# - In this file we have an incomplete skeleton of
# a neural network implementation.  Follow the online instructions
# and complete the NotImplemented methods below.
#

import math
import random


class ValuedElement(object):
    """
    This is an abstract class that all Network elements inherit from
    """

    def __init__(self, name, val):
        self.my_name = name
        self.my_value = val

    def set_value(self, val):
        self.my_value = val

    def get_value(self):
        return self.my_value

    def get_name(self):
        return self.my_name

    def __repr__(self):
        return "%s(%s)" % (self.my_name, self.my_value)


class DifferentiableElement(object):
    """
    This is an abstract interface class implemented by all Network
    parts that require some differentiable element.
    """

    def output(self):
        raise NotImplementedError, "This is an abstract method"

    def dOutdX(self, elem):
        raise NotImplementedError, "This is an abstract method"

    def clear_cache(self):
        """clears any precalculated cached value"""
        pass


class Input(ValuedElement, DifferentiableElement):
    """
    Representation of an Input into the network.
    These may represent variable inputs as well as fixed inputs
    (Thresholds) that are always set to -1.
    """

    def __init__(self, name, val):
        ValuedElement.__init__(self, name, val)
        DifferentiableElement.__init__(self)

    def output(self):
        """
        Returns the output of this Input node.
        
        returns: number (float or int)
        """
        return ValuedElement.get_value(self)

    def dOutdX(self, elem):
        """
        Returns the derivative of this Input node with respect to 
        elem.

        elem: an instance of Weight

        returns: number (float or int)
        """
        return 0


class Weight(ValuedElement):
    """
    Representation of an weight into a Neural Unit.
    """

    def __init__(self, name, val):
        ValuedElement.__init__(self, name, val)
        self.next_value = None

    def set_next_value(self, val):
        self.next_value = val

    def update(self):
        self.my_value = self.next_value


class Neuron(DifferentiableElement):
    """
    Representation of a single sigmoid Neural Unit.
    """

    def __init__(self, name, inputs, input_weights, use_cache=True):
        assert len(inputs) == len(input_weights)
        for i in range(len(inputs)):
            assert isinstance(inputs[i], (Neuron, Input))
            assert isinstance(input_weights[i], Weight)
        DifferentiableElement.__init__(self)
        self.my_name = name
        self.my_inputs = inputs  # list of Neuron or Input instances
        self.my_weights = input_weights  # list of Weight instances
        self.use_cache = use_cache
        self.clear_cache()
        self.my_descendant_weights = None

    def get_descendant_weights(self):
        """
        Returns a mapping of the names of direct weights into this neuron,
        to all descendant weights.
        """
        if self.my_descendant_weights is None:
            self.my_descendant_weights = {}
            inputs = self.get_inputs()
            weights = self.get_weights()
            for i in xrange(len(weights)):
                weight = weights[i]
                weight_name = weight.get_name()
                self.my_descendant_weights[weight_name] = set()
                input = inputs[i]
                if not isinstance(input, Input):
                    descendants = input.get_descendant_weights()
                    for name, s in descendants.items():
                        st = self.my_descendant_weights[weight_name]
                        st = st.union(s)
                        st.add(name)
                        self.my_descendant_weights[weight_name] = st

        return self.my_descendant_weights

    def isa_descendant_weight_of(self, target, weight):
        """
        Checks if [target] is a indirect input weight into this Neuron
        via the direct input weight [weight].
        """
        weights = self.get_descendant_weights()
        if weight.get_name() in weights:
            return target.get_name() in weights[weight.get_name()]
        else:
            raise Exception("weight %s is not connect to this node: %s"
                            % (weight, self))

    def has_weight(self, weight):
        """
        Checks if [weight] is a direct input weight into this Neuron.
        """
        weights = self.get_descendant_weights()
        return weight.get_name() in self.get_descendant_weights()

    def get_weight_nodes(self):
        return self.my_weights

    def clear_cache(self):
        self.my_output = None
        self.my_doutdx = {}

    def output(self):
        # Implement compute_output instead!!
        if self.use_cache:
            # caching optimization, saves previously computed dOutDx.
            if self.my_output is None:
                self.my_output = self.compute_output()
            return self.my_output
        return self.compute_output()

    def compute_output(self):
        """
        Returns the output of this Neuron node, using a sigmoid as
        the threshold function.

        returns: number (float or int)
        """

        # loop through and sum all the weighted inputs
        z = 0
        for idx, i in enumerate(self.my_inputs):
            # print 'Input Neuron name:' + i.get_name()
            # print 'Input Weight name:' + self.my_weights[idx].get_name()
            z += i.output() * self.my_weights[idx].get_value()

        o = 1 / (1 + math.exp(-1 * z))

        return o

    def dOutdX(self, elem):
        # Implement compute_doutdx instead!!
        if self.use_cache:
            # caching optimization, saves previously computed dOutDx.
            if elem not in self.my_doutdx:
                self.my_doutdx[elem] = self.compute_doutdx(elem)
            return self.my_doutdx[elem]
        return self.compute_doutdx(elem)

    def compute_doutdx(self, elem):
        """
        Returns the derivative of this Neuron node, with respect to weight
        elem, calling output() and/or dOutdX() recursively over the inputs.

        elem: an instance of Weight

        returns: number (float/int)
        """
        # print elem
        # print self.my_weights
        # print self.get_descendant_weights()

        output = self.output()

        # base case
        if self.has_weight(elem):
            # print "We're in the base case with: " + elem.get_name()
            # fetch the input value corresponding to the weight
            return output * (1 - output) * self.my_inputs[self.my_weights.index(elem)].output()

        else:
            # print "We're trying to recurse with: " + elem.get_name()
            # need to recurse, gotta find which weight object is the right one
            chain_rule = 0
            for weight in self.my_weights:
                if self.isa_descendant_weight_of(elem, weight):
                    chain_rule += weight.get_value() * self.my_inputs[self.my_weights.index(weight)].dOutdX(elem)

            return self.compute_output() * (1 - self.compute_output()) * chain_rule

    def get_weights(self):
        return self.my_weights

    def get_inputs(self):
        return self.my_inputs

    def get_name(self):
        return self.my_name

    def __repr__(self):
        return "Neuron(%s)" % (self.my_name)


class PerformanceElem(DifferentiableElement):
    """
    Representation of a performance computing output node.
    This element contains methods for setting the
    desired output (d) and also computing the final
    performance P of the network.

    This implementation assumes a single output.
    """

    def __init__(self, input, desired_value):
        assert isinstance(input, (Input, Neuron))
        DifferentiableElement.__init__(self)
        self.my_input = input
        self.my_desired_val = desired_value

    def output(self):
        """
        Returns the output of this PerformanceElem node.
        
        returns: number (float/int)
        """

        # Get the output value of the final Neuron
        output = self.my_input.compute_output()

        # Compute the Performance
        P = -0.5 * (self.my_desired_val - output) ** 2
        return P

    def dOutdX(self, elem):
        """
        Returns the derivative of this PerformanceElem node with respect
        to some weight, given by elem.

        elem: an instance of Weight

        returns: number (int/float)
        """
        # print self.my_desired_val
        # print self.my_input.compute_output()
        # print self.my_input.compute_doutdx(elem)
        return (self.my_desired_val - self.my_input.compute_output()) * self.my_input.compute_doutdx(elem)

    def set_desired(self, new_desired):
        self.my_desired_val = new_desired

    def get_input(self):
        return self.my_input


def alphabetize(x, y):
    if x.get_name() > y.get_name():
        return 1
    return -1


class Network(object):
    def __init__(self, performance_node, neurons):
        self.inputs = []
        self.weights = []
        self.performance = performance_node
        self.output = performance_node.get_input()
        self.neurons = neurons[:]
        self.neurons.sort(cmp=alphabetize)
        for neuron in self.neurons:
            self.weights.extend(neuron.get_weights())
            for i in neuron.get_inputs():
                if isinstance(i, Input) and not i.get_name() == 'i0' and not i in self.inputs:
                    self.inputs.append(i)
        self.weights.reverse()
        self.weights = []
        for n in self.neurons:
            self.weights += n.get_weight_nodes()

    def clear_cache(self):
        for n in self.neurons:
            n.clear_cache()


def seed_random():
    """Seed the random number generator so that random
    numbers are deterministically 'random'"""
    random.seed(0)


def random_weight():
    """Generate a deterministic random weight"""
    # We found that random.randrange(-1,2) to work well emperically 
    # even though it produces randomly 3 integer values -1, 0, and 1.
    return random.randrange(-1, 2)

    # Uncomment the following if you want to try a uniform distribuiton 
    # of random numbers compare and see what the difference is.
    # return random.uniform(-1, 1)


def make_neural_net_basic():
    """
    Constructs a 2-input, 1-output Network with a single neuron.
    This network is used to test your network implementation
    and a guide for constructing more complex networks.

    Naming convention for each of the elements:

    Input: 'i'+ input_number
    Example: 'i1', 'i2', etc.
    Conventions: Start numbering at 1.
                 For the -1 inputs, use 'i0' for everything

    Weight: 'w' + from_identifier + to_identifier
    Examples: 'w1A' for weight from Input i1 to Neuron A
              'wAB' for weight from Neuron A to Neuron B

    Neuron: alphabet_letter
    Convention: Order names by distance to the inputs.
                If equal distant, then order them left to right.
    Example:  'A' is the neuron closest to the inputs.

    All names should be unique.
    You must follow these conventions in order to pass all the tests.
    """
    i0 = Input('i0', -1.0)  # this input is immutable
    i1 = Input('i1', 0.0)
    i2 = Input('i2', 0.0)

    w1A = Weight('w1A', 1)
    w2A = Weight('w2A', 1)
    wA = Weight('wA', 1)

    # Inputs must be in the same order as their associated weights
    A = Neuron('A', [i1, i2, i0], [w1A, w2A, wA])
    P = PerformanceElem(A, 0.0)

    net = Network(P, [A])
    return net


def make_neural_net_two_layer():
    """
    Create a 2-input, 1-output Network with three neurons.
    There should be two neurons at the first level, each receiving both inputs
    Both of the first level neurons should feed into the second layer neuron.

    See 'make_neural_net_basic' for required naming convention for inputs,
    weights, and neurons.
    """

    seed_random()

    i0 = Input('i0', -1.0)  # this input is immutable
    i1 = Input('i1', 0.0)
    i2 = Input('i2', 0.0)

    # Input Weights
    wts = [random_weight() for i in range(0, 9)]

    w1A = Weight('w1A', wts[0])
    w2A = Weight('w2A', wts[1])
    w1B = Weight('w1B', wts[2])
    w2B = Weight('w2B', wts[3])

    # Inner Layer Weights
    wAC = Weight('wAC', wts[4])
    wBC = Weight('wBC', wts[5])

    # Immutable input weights
    wA = Weight('wA', wts[6])
    wB = Weight('wB', wts[7])
    wC = Weight('wC', wts[8])

    # Inputs must be in the same order as their associated weights
    A = Neuron('A', [i1, i2, i0], [w1A, w2A, wA])
    B = Neuron('B', [i1, i2, i0], [w1B, w2B, wB])
    C = Neuron('C', [A, B, i0], [wAC, wBC, wC])
    P = PerformanceElem(C, 0.0)

    net = Network(P, [A, B, C])
    return net


def make_neural_net_challenging():
    """
    Design a network that can in-theory solve all 3 problems described in
    the lab instructions.  Your final network should contain
    at most 5 neuron units.

    See 'make_neural_net_basic' for required naming convention for inputs,
    weights, and neurons.
    """

    seed_random()

    i0 = Input('i0', -1.0)  # this input is immutable
    i1 = Input('i1', 0.0)
    i2 = Input('i2', 0.0)

    # Input Weights
    wts = [random_weight() for i in range(0, 15)]

    w1A = Weight('w1A', wts[0])
    w2A = Weight('w2A', wts[1])
    w1B = Weight('w1B', wts[2])
    w2B = Weight('w2B', wts[3])

    # Second Layer Weights
    wAC = Weight('wAC', wts[4])
    wAD = Weight('wAD', wts[5])
    wBC = Weight('wBC', wts[6])
    wBD = Weight('wDB', wts[7])

    # Third Layer Weights
    wCE = Weight('wCE', wts[8])
    wDE = Weight('wDE', wts[9])

    # Immutable input weights
    wA = Weight('wA', wts[10])
    wB = Weight('wB', wts[11])
    wC = Weight('wC', wts[12])
    wD = Weight('wD', wts[13])
    wE = Weight('wE', wts[14])

    # Inputs must be in the same order as their associated weights
    A = Neuron('A', [i1, i2, i0], [w1A, w2A, wA])
    B = Neuron('B', [i1, i2, i0], [w1B, w2B, wB])
    C = Neuron('C', [A, B, i0], [wAC, wBC, wC])
    D = Neuron('D', [A, B, i0], [wAD, wBD, wD])
    E = Neuron('E', [C, D, i0], [wCE, wDE, wE])
    P = PerformanceElem(E, 0.0)

    net = Network(P, [A, B, C, D, E])
    return net


def make_neural_net_with_weights():
    """
    In this method you are to use the network you designed earlier
    and set pre-determined weights.  Your goal is to set the weights
    to values that will allow the "patchy" problem to converge quickly.
    Your output network should be able to learn the "patchy"
    dataset within 1000 iterations of back-propagation.
    """
    # You can preset weights for the network by completing
    # and uncommenting the init_weights dictionary below.
    #
    # init_weights = { 'w1A' : 0.0,
    #                  'w2A' : 0.0,
    #                  'w1B' : 0.0,
    #                  'w2B' : 0.0,
    #                  .... # finish me!
    #
    init_weights = {'w1A': 2.762708,
                    'w2A': 2.762346,
                    'wA': 6.905249,
                    'w1B': -2.631801,
                    'w2B': -2.633044,
                    'wB': -14.182442,
                    'wAC': -9.019906,
                    'wBC': 3.963480,
                    'wC': -0.221470,
                    'wAD': 2.370158,
                    'wDB': -8.312999,
                    'wD': -1.039751,
                    'wCE': 9.285383,
                    'wDE': 9.546696,
                    'wE': 4.589401
                    }
    return make_net_with_init_weights_from_dict(make_neural_net_challenging,
                                                init_weights)


def make_net_with_init_weights_from_dict(net_fn, init_weights):
    net = net_fn()
    for w in net.weights:
        w.set_value(init_weights[w.get_name()])
    return net


def make_net_with_init_weights_from_list(net_fn, init_weights):
    net = net_fn()
    for i in range(len(net.weights)):
        net.weights[i].set_value(init_weights[i])
    return net


def abs_mean(values):
    """Compute the mean of the absolute values a set of numbers.
    For computing the stopping condition for training neural nets"""
    abs_vals = map(lambda x: abs(x), values)
    total = sum(abs_vals)
    return total / float(len(abs_vals))


def train(network,
          data,  # training data
          rate=1.0,  # learning rate
          target_abs_mean_performance=0.0001,
          max_iterations=10000,
          verbose=True):
    """Run back-propagation training algorithm on a given network.
    with training [data].   The training runs for [max_iterations]
    or until [target_abs_mean_performance] is reached.
    """
    iteration = 0
    while iteration < max_iterations:
        fully_trained = False
        performances = []  # store performance on each data point
        for datum in data:
            # set network inputs
            for i in xrange(len(network.inputs)):
                network.inputs[i].set_value(datum[i])

            # set network desired output
            network.performance.set_desired(datum[-1])

            # clear cached calculations
            network.clear_cache()

            # compute all the weight updates
            for w in network.weights:
                w.set_next_value(w.get_value() +
                                 rate * network.performance.dOutdX(w))

            # set the new weights
            for w in network.weights:
                w.update()

            # save the performance value
            performances.append(network.performance.output())

            # clear cached calculations
            network.clear_cache()

        # compute the mean performance value
        abs_mean_performance = abs_mean(performances)

        if abs_mean_performance < target_abs_mean_performance:
            if verbose:
                print "iter %d: training complete.\n" \
                      "mean-abs-performance threshold %s reached (%1.6f)" \
                      % (iteration,
                         target_abs_mean_performance,
                         abs_mean_performance)
            break

        iteration += 1
        if iteration % 1000 == 0 and verbose:
            print "iter %d: mean-abs-performance = %1.6f" \
                  % (iteration,
                     abs_mean_performance)


def test(network, data, verbose=True):
    """Test the neural net on some given data."""
    correct = 0
    for datum in data:

        for i in range(len(network.inputs)):
            network.inputs[i].set_value(datum[i])

        # clear cached calculations
        network.clear_cache()
        result = network.output.output()
        network.clear_cache()

        rounded_result = round(result)
        if round(result) == datum[-1]:
            correct += 1
            if verbose:
                print "test(%s) returned: %s => %s [%s]" % (str(datum),
                                                            str(result),
                                                            rounded_result,
                                                            "correct")
        else:
            if verbose:
                print "test(%s) returned: %s => %s [%s]" % (str(datum),
                                                            str(result),
                                                            rounded_result,
                                                            "wrong")

    return float(correct) / len(data)
