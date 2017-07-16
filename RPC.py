# Title: Reverse Polish Calculator (as a nn)
# Author: Matthew Bird
# Data: 5/18/2017
# Notes: in pursuit of a non-uniform non-linear layer as well as selective recurrance

from Number import *

xfr_fxns = [np.sin, np.cos, np.arctan, np.tanh, np.arcsinh]
red_fxns = [np.subtract, np.add, np.divide, np.multiply]


def get_count(x):
    """
    :param x:
    :return:
    """
    if floats(x):
        return 1
    elif x in xfr_fxns:
        return 0
    if x in red_fxns:
        return -1


def floats(x):
    """
    function to tell if x can be typed as float
    :param x: input
    :return: bool
    """
    if isinstance(x, Number):
        return True
    try:
        float(x)
        return True
    except:
        return False


def translate(x):
    if floats(x):
        # TODO: If type == Input() class then return x
        return float(x)
    elif x[:2] == 'n':
        return Number(min_range=-10, max_range=10, bucket_count=100)
    elif x == "-":
        return np.subtract
    elif x == "+":
        return np.add
    elif x == "/":
        return np.divide
    elif x == "*":
        return np.multiply
    elif x == "pow":
        return np.power
    elif x == "sin":
        return np.sin
    elif x == "cos":
        return np.cos
    elif x == "tan":
        return np.tan
    elif x == "exp":
        return np.exp


class Element:
    def __init__(self, e):
        self.item = translate(e)
        self.lock = False
        items = [Number(min_range=-10, max_range=10, bucket_count=100)] + xfr_fxns + red_fxns
        self.buckets = []
        for i in items:
            self.buckets.append({'item': i, 'last_sample': None, 'x_samples': [], 'scores': [], 'avg': None})
            if isinstance(i, Number):
                self.number_bucket = self.buckets[-1]
        self.lastest_bucket = None


    def count(self):
        return get_count(self.item)


class Calculator:
    def __init__(self):
        self.data = []  # n-dimensional array
        self.target = []  # one dimensional array
        self.elements = []  # array of polish calculator elements

    def set_function(self, string):
        self.elements = string.split()
        for i, e in enumerate(self.elements):
            self.elements[i] = Element(e)

    def evaluate(self, v=0):
        """
        take the self.elements and evaluate it as a RPC
        :return:
        """
        if v >0:
            print(str(self))
        my_list = []
        for e in self.elements:
            if floats(e.item):
                # TODO: if type == Input() class then append e.item() instead
                if isinstance(e.item, Number):
                    my_list.append(e.item())
                else:
                    my_list.append(e.item)
            elif get_count(e.item) == -1:
                my_list = [e.item(*my_list)]
            elif get_count(e.item) == 0:
                my_list = my_list[:-1] + [e.item(my_list[-1])]
            if v>0:
                print my_list
        return my_list

    def validate(self, locked_only=False):
        possible_counts = {0}
        for e in self.elements:
            if e.lock or not locked_only:
                possible_counts = set([count + e.count() for count in possible_counts]) & {1, 2}
            else:
                if {2} == possible_counts:
                    two_found = True
                else:
                    two_found = False
                add_one = set([count + 1 for count in possible_counts])
                subtract_one = set([count - 1 for count in possible_counts])
                possible_counts = (add_one | possible_counts | subtract_one) & {1, 2}
                if two_found:
                    possible_counts -= {2}
            if not possible_counts & {1, 2}:
                return False
        if 1 not in possible_counts:
            return False
        else:
            return True
        #return bool(possible_counts)

    def lock(self, indices):
        for i in indices:
            self.elements[i].lock = True

    def unlock(self, indices):
        for i in indices:
            self.elements[i].lock = False

    def can_become(self, index):
        prev_item = self.elements[index].item
        prev_lock = self.elements[index].lock
        self.elements[index].lock = True
        possibles = []

        self.elements[index].item = xfr_fxns[0]
        if self.validate(locked_only=True):
            possibles += xfr_fxns
        self.elements[index].item = red_fxns[0]
        if self.validate(locked_only=True):
            possibles += red_fxns
        self.elements[index].item = 1.0
        if self.validate(locked_only=True):
            # TODO: This then becomes a new random Number() or Input() chosen from input list <-- start here
            possibles += [Number(min_range=-10, max_range=10, bucket_count=100)]

        self.elements[index].item = prev_item
        self.elements[index].lock = prev_lock

        return possibles

    def randomize_unlocked(self, v=1):
        indexes = range(len(self.elements))
        random.shuffle(indexes)
        indexes = [i for i in indexes if not self.elements[i].lock]
        for i in indexes:
            if v>0:
                print([j.item for j in self.elements])
            can_be = self.can_become(i)
            possible_buckets = []
            for b in self.elements[i].buckets:
                if b['item'] in can_be:
                    possible_buckets.append(b)
                elif isinstance(b['item'], Number):
                    possible_buckets.append(self.elements[i].number_bucket)
            self.elements[i].latest_bucket = bandit_choice(possible_buckets, key='avg')
            self.elements[i].item = self.elements[i].latest_bucket['item']
            self.elements[i].lock = True

    def __str__(self):
        return str([e.item for e in self.elements])


if __name__ == "__main__":
    # # test 1
    # C = Calculator()
    # C.set_function("1 2 sin + 2 - sin 8")
    # C.lock([0, 1, 2, 3, 4, 5, 6,7])
    # C.unlock([1, 3])
    # print C.validate()
    # print C.evaluate()
    # print C.can_become(4)
    # test 2
    C = Calculator()
    C.set_function("1 0 0 0 0 0")
    # C.lock([0])
    C.randomize_unlocked()
    print(C.evaluate(v=1))
    # TODO: add Number class (with __float__ and __str__)
    # TODO: add Input class (with __float__ and __str__)
    # TODO: Recurrance & deltas & polyporph
    # TODO: gradient descent
    # TODO: Parallelize
    # TODO: Teachers and learners
    # TODO: Functional Decomp as seed
