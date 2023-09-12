# nodes used for graph search DFS or BFS, the self parameter and declarations are used to so that the variables
# be accessed within the function and outside if made public
class Node():
    def __init__(self, state, parent, action):
        self.state = state  # current position in the tree or data structure
        self.parent = parent # points to node that led to this node
        self.action = action  # action taken to get to the node


class StackFrontier():
    # the init is the constructor and self allows the frontier to be accessed within/outside the function
    def __init__(self):
        self.frontier = []

    # appends a node to the end of the frontier
    def add(self, node):
        self.frontier.append(node)

    # citerates over all nodes and checks the state(actor) is not already in the frontier
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # checks if frontier empty

    def empty(self):
        return len(self.frontier) == 0

    # this is stack pop DFS that puts the current node as the node from the end of the frontier -1
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# this inherits everything from the DFS but overrides the remove to act like a queue
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]  # this one takes the current node as the front of the fronteir 1
            return node
