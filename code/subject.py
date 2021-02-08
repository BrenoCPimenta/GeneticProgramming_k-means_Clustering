import math
import numpy as np
import copy

class SubjectTree():
    variable_counter = 0
    constant_prob = [0.1, 0.9]
    min_constant = -10
    max_constant = 10
    
    def __init__(self, size, seed, index, operators, operators_prob, constant_prob=None, constant_limits=None):
        SubjectTree.variable_counter = 0
        self.seed = seed + index
        
        #Set probability of constants in terminal nodes
        if constant_prob is not None:
            SubjectTree.constant_prob = constant_prob
        if constant_limits is not None:
            SubjectTree.min_constant, SubjectTree.max_constant = constant_limits
        #Create tree:
        np.random.seed(self.seed)
        self.root = Node(size, operators, operators_prob)
        
    
    def printFunction(self, variable_values):
        return self.root.printRecursion(variable_values)
    
    def evalFunction(self, variable_values):
        return self.root.evalRecursion(variable_values)

    def getDepth(self):
        return self.root.getNodeDepth()

    def mutate(self):
        depth = self.root.getNodeDepth()
        mutation_depth = np.random.randint(depth+1)
        self.root.mutate(mutation_depth)

    def getSlice(self, depth_change):
        return self.root.getSubTree(depth_change)

    def transplant(self, new_node, depth_change):
        return self.root.setSubTree(new_node, depth_change)

class Node(SubjectTree):
    def __init__(self, num_layer, operators, operators_prob):        
        self.num_layer = num_layer
        self.operators = operators
        self.operators_prob = operators_prob

        #Leaf
        if self.num_layer <= 0:
            self.node_type = 'terminal'
            self.terminal_type = np.random.choice(
                ['constant', 'variable'], 
                p=SubjectTree.constant_prob)
            
            #set terminal value
            if self.terminal_type == 'variable':
                #only sets the position
                self.variable_number = SubjectTree.variable_counter
                SubjectTree.variable_counter += 1
            else:
                self.variable_number = self._calculateConstant()
            #Leaf properties:
            self.node_funciton = None
            self.left_node = None
            self.right_node = None
            
        #InnerNode
        else:
            self.node_type = 'function'
            self.node_funciton = np.random.choice(operators, p=operators_prob)
            
            #InnerNode properties:
            self.terminal_type = None
            self.variable_number = None
            self.left_node = Node(num_layer - 1, operators, operators_prob)
            self.right_node = Node(num_layer - 1, operators, operators_prob)

    def getNodeDepth(self):
        if self.node_type == 'terminal' or self.left_node == None:
            return 1
        else:
            return self.left_node.getNodeDepth() + 1
    
    def getSubTree(self, depth_change):
        result = {"search_status" : "still_on_search", "root" : None}

        if depth_change == 0 and self.node_type != 'terminal':
            result['search_status'] = "write_last_node"
            return result
        elif depth_change == 0 and self.node_type == 'terminal':
            result['search_status'] = "last_terminal"
            return result

        #else:
        side_decision = np.random.choice(['left', 'right'])
        if side_decision == 'left':
            if self.left_node is None:
                return {"search_status" : "last_terminal", "root" : None}
            else:
                recursion_result = self.left_node.getSubTree(depth_change - 1)

        elif side_decision == 'right':
            if self.right_node is None:
                return {"search_status" : "last_terminal", "root" : None}
            else:
                recursion_result = self.right_node.getSubTree(depth_change - 1)
        else:
            raise "getSubTree side decision problem"

        if recursion_result['search_status'] == 'last_terminal':
            recursion_result['search_status'] == 'write_last_node'
            return recursion_result
        elif recursion_result['search_status'] == 'write_last_node':
            if side_decision == 'left':
                new_root = copy.deepcopy(self.left_node)
                return {"search_status" : "Found", "root" : new_root}
            else:
                new_root = copy.deepcopy(self.right_node)
                return {"search_status" : "Found", "root" : new_root}
        elif recursion_result['search_status'] == 'Found':
            return recursion_result
        else:
            raise "getSubTree search_status problem"
        

    def setSubTree(self, new_node, depth_change):
        side_decision = np.random.choice(['left', 'right'])

        if self.left_node == None or self.right_node == None:
            return 'terminal'
        elif depth_change == 0:
            if side_decision == 'left':
                self.left_node = new_node
                return 'setted'
            else:
                self.right_node = new_node
                return 'setted'
        else:
            if side_decision == 'left':
                result = self.left_node.setSubTree(new_node, depth_change-1)
            else:
                result = self.right_node.setSubTree(new_node, depth_change-1)

            if result == 'setted':
                return 'setted'
            else:
                if side_decision == 'left':
                    self.left_node = new_node
                    return 'setted'
                else:
                    self.right_node = new_node
                    return 'setted'


    def mutate(self, depth):
        if depth != 0 and self.left_node != None and self.right_node != None: #keep digging
            side_decision = np.random.choice(['left', 'right'])
            if side_decision == 'left':
                self.left_node.mutate(depth - 1)
            elif side_decision == 'right':
                self.right_node.mutate(depth - 1)
            else:
                raise "mutate point side decision problem"
        else: #Mutate
            if self.node_type == 'function':
                self.node_funciton = np.random.choice(self.operators, p=self.operators_prob)
            elif self.node_type == 'terminal':
                self.terminal_type = np.random.choice(
                    ['constant', 'variable'], 
                    p=SubjectTree.constant_prob)
                 #set terminal value
                if self.terminal_type == 'variable':
                    #only sets the position
                    self.variable_number = SubjectTree.variable_counter
                    SubjectTree.variable_counter += 1
                else:
                    self.variable_number = self._calculateConstant()
            else:
                raise "mutate point type problem"

    def printRecursion(self, variable_values, position=None):
        #Call inner left nodes:
        if self.left_node is not None:
            self.left_node.printRecursion(variable_values, 'left')
        #Print node content:
        if self.node_type == 'function':
            print(self.node_funciton, end =" ")
        elif self.node_type == 'terminal':
            if self.terminal_type == 'variable':
                variable_position = self.variable_number % len(variable_values)
                
                if position == 'left':
                    print("(", variable_values[variable_position], end=" ")
                else:
                    print(variable_values[variable_position], ")", end=" ")
            else: #constant
                if position == 'left':
                    print("(", self.variable_number, end=" ")
                else:
                    print(self.variable_number, ")", end=" ")
        #Call inner right nodes
        if self.right_node is not None:
            self.right_node.printRecursion(variable_values, 'right')
            
        
    def evalRecursion(self, variable_values):
        if self.node_type == 'terminal':
            if self.terminal_type == 'variable':
                variable_position = self.variable_number % len(variable_values)
                return variable_values[variable_position]
            else: #constant
                return self.variable_number
        elif self.node_type == 'function':
            if self.left_node == None or self.right_node == None:
                #print("--------------------------------------------------------------")
                return 0
            else:
                left_value = self.left_node.evalRecursion(variable_values)
                right_value = self.right_node.evalRecursion(variable_values)
            
            #print("   -> ", left_value, " ", self.node_funciton, "  ", right_value, "  =", end=" ")
            return_value = 0
            if self.node_funciton == '+':
                try:
                    return_value = left_value + right_value
                except:
                    return_value = 0
            elif self.node_funciton == '-':
                try:
                    return_value = left_value - right_value
                except:
                    return_value = 0
            elif self.node_funciton == '*':
                try:
                    return_value = left_value * right_value
                except:
                    return_value = 0
            elif self.node_funciton == '/':
                try:
                    if right_value == 0:
                        return_value = 0
                    else:
                        return_value = left_value / right_value
                except:
                    return_value = 0
            elif self.node_funciton == 'log':
                try:
                    return_value = left_value * math.log(abs(right_value))
                except:
                    try:
                        return_value = round(abs(left_value),0) * math.log(round(abs(right_value),0))
                    except:
                        return_value = 0
                    
            elif self.node_funciton == 'sin':
                try:
                    return_value = left_value * math.sin(right_value)
                except:
                    try:
                        return_value = round(abs(left_value),0) * math.sin(round(abs(right_value),0))
                    except:
                        return_value = 0

            elif self.node_funciton == 'cos':
                try:
                    return_value = left_value * math.cos(right_value)
                except:
                    try:
                        return_value = round(abs(left_value),0) * math.cos(abs(round(right_value,0)))
                    except:
                        return_value = 0                
            elif self.node_funciton == 'sqrt':
                try:
                    return_value = left_value * math.sqrt(right_value)
                except:
                    try:
                        return_value = round(abs(left_value),0) * math.sqrt(abs(round(right_value,0)))
                    except:
                        return_value = 0
            elif self.node_funciton == '^':
                try:
                    if right_value == 0 or left_value == 0:
                        return_value = 0
                    elif abs(right_value) > 30:
                        return_value = left_value
                    else:
                        return_value = round(abs(left_value),0) ** round(abs(right_value),0)
                except:
                    try:
                        return_value = round(abs(left_value),0) ** round(abs(right_value),0)
                    except:
                        return_value = 0
            else:
                raise 'evalRecursion invalid node_funciton'

            if return_value > 10000000000000000000:
                return 0
            else:
                return return_value 
        else:
            raise 'evalRecursion invalid node_type'
        
    def _calculateConstant(self):
        return round(
            np.random.uniform(
                SubjectTree.min_constant,
                SubjectTree.max_constant),
            2)