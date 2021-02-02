import pandas as pd
from statistics import mean

from fitness import FitnessCLustering
from inicialization import ramped_half_and_half
from selection import elitistTournament


#Set parameters for model
parameters = {
    "seed" : 0,
    "population_size" : 7,
    "max_tree_depth" : 7,
    "generations" : 1,
    "tournament_window" : 3,
    "point1" : [1,2,3],
    "point2" : [4,5,6],
    "cross_prob" : 0.7,
    "mutation_prob" : 0.3,
    "functions" : ['+','-','*','/','log','sin','cos','sqrt', '^'],
    "functions_prob" : [0.15,0.15,0.25,0.01,0.08, 0.15,0.15,0.05, 0.01]
}

#Get cancer data
df_cancer_train = pd.read_csv('data/breast_cancer_coimbra_train.csv')
df_cancer_test = pd.read_csv('data/breast_cancer_coimbra_train.csv')
df_cancer_train_X = df_cancer_train.drop(['Classification'], axis=1)
df_cancer_train_Y = df_cancer_train['Classification']
df_cancer_test_X = df_cancer_test.drop(['Classification'], axis=1)
df_cancer_test_Y = df_cancer_test['Classification']


#Initialize population
population = ramped_half_and_half(
                seed=parameters['seed'],
                population_size=parameters['population_size'],
                max_size=parameters['max_tree_depth'],
                operators=parameters['functions'],
                operators_prob=parameters['functions_prob'],
                constant_prob=None,
                constant_limits=None)

#Run generations
generation_results = {}
for i in range(parameters['generations']):
    population_results = []
    for j in range(len(population)):
        result = FitnessCLustering(2,df_cancer_train_X,df_cancer_train_Y, False, population[j])
        population_results.append(result)
    best_result = max(population_results)
    worst_result = min(population_results)
    mean = mean(population_results)
    generation_results[i] = [best_result, mean, worst_result]
    champions = elitistTournament(
                    window=parameters['tournament_window'],
                    population=population,
                    results=population_results)
    print("/n")
    champions = elitistTournament(
                    window=parameters['tournament_window'],
                    population=population_results,
                    results=population_results)
    print("/n")  
    champions = elitistTournament(
                    window=parameters['tournament_window'],
                    population=['a','b','c','d','e','f'],
                    results=[1,2,3,4,5,6])                  

