from subject import SubjectTree
import numpy as np
import copy


def newPopulationGenerator(winners_subjects, population_size, cross_mutation_prob, max_tree_depth):
    cnt_winners = len(winners_subjects)
    if cnt_winners >= population_size:
        raise "newPopulationGenerator: Number of winners don't match population size"

    #Add winners to new generation:
    new_population = []
    for i in range(cnt_winners):
        new_population.append(winners_subjects[i])
    
    #Create new operated subjects from winners
    while len(new_population) < population_size:
        operator = np.random.choice(
                        ['crossover', 'mutation'], 
                        p=cross_mutation_prob)
        first_winner_to_operate = np.random.randint(cnt_winners)
        if operator == 'mutation':
            new_subject = copy.deepcopy(winners_subjects[first_winner_to_operate])
            new_subject.mutate()
        elif operator == 'crossover':
            second_winner_to_operate = first_winner_to_operate
            while second_winner_to_operate == first_winner_to_operate:
                second_winner_to_operate = np.random.randint(cnt_winners)
            new_subject = crossover(subject_donnor=winners_subjects[first_winner_to_operate],
                                    subject_donee=winners_subjects[second_winner_to_operate],
                                    max_tree_depth=max_tree_depth)
        else:
            raise 'newPopulationGenerator: operator selection problem'
        new_population.append(new_subject)
    return new_population


def crossover(subject_donnor, subject_donee, max_tree_depth):
    #Find tree layer and chop a sub-tree
    slice_depth = np.random.randint(max_tree_depth - 1) + 1
    tree_slice = subject_donnor.getSlice(slice_depth)
    #Create and return a new subject with a subtree transplanted
    new_subject = copy.deepcopy(subject_donee)
    new_subject.transplant(tree_slice['root'], slice_depth)
    return new_subject