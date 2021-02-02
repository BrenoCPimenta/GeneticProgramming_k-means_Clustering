from subject import SubjectTree

def ramped_half_and_half(
    seed,
    population_size,
    max_size,
    operators,
    operators_prob,
    constant_prob=None,
    constant_limits=None):
    
    #Calculating number of subjects with which size of trees
    trees_in_layers = int(population_size/(max_size - 1))
    trees_rest = int(population_size%(max_size - 1))
    trees_in_last_layer = trees_in_layers + trees_rest
    
    #Creating population
    population = []
    cnt = 0
    for i in range(2, max_size+1):
        #Creating trees with number of layers smaller than max
        if i != max_size:
            for j in range(trees_in_layers):
                temp_tree = SubjectTree(
                    size= i ,
                    seed=seed,
                    index=cnt,
                    operators=operators,
                    operators_prob=operators_prob,
                    constant_prob=constant_prob,
                    constant_limits=constant_limits)
                population.append(temp_tree)
                cnt += 1
        #Creating trees with max depth
        else:
            for j in range(trees_in_last_layer):
                temp_tree = SubjectTree(
                    size= i ,
                    seed=seed,
                    index=cnt,
                    operators=operators,
                    operators_prob=operators_prob,
                    constant_prob=constant_prob,
                    constant_limits=constant_limits)
                population.append(temp_tree)
                cnt += 1
    
    return population
