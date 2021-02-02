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
        

class Node(SubjectTree):
    def __init__(self, num_layer, operators, operators_prob):        

        #Leaf
        if num_layer <= 0:
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
            left_value = self.left_node.evalRecursion(variable_values)
            right_value = self.right_node.evalRecursion(variable_values)
            
            #print("   -> ", left_value, " ", self.node_funciton, "  ", right_value, "  =", end=" ")
    
            if self.node_funciton == '+':
                return left_value + right_value
            elif self.node_funciton == '-':
                return left_value - right_value
            elif self.node_funciton == '*':
                return left_value * right_value
            elif self.node_funciton == '/':
                if right_value == 0:
                    return 0
                else:
                    return left_value / right_value
            elif self.node_funciton == 'log':
                if right_value == 0:
                    return 0
                else:
                    return left_value * math.log(abs(right_value))
            elif self.node_funciton == 'sin':
                #print(left_value * math.sin(right_value))
                return left_value * math.sin(right_value)
            elif self.node_funciton == 'cos':
                #print(left_value * math.cos(right_value))
                return left_value * math.cos(right_value)
            elif self.node_funciton == 'sqrt':
                return left_value * math.sqrt(abs(round(right_value,0)))
            elif self.node_funciton == '^':
                return left_value ** right_value
            else:
                raise 'evalRecursion invalid node_funciton'
        else:
            raise 'evalRecursion invalid node_type'
        
    def _calculateConstant(self):
        return round(
            np.random.uniform(
                SubjectTree.min_constant,
                SubjectTree.max_constant),
            2)
