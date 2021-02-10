import pandas as pd
import numpy as np
import json
from statistics import mean

from fitness import FitnessCLustering
from inicialization import ramped_half_and_half
from selection import elitistTournament
from genetic_diversity import newPopulationGenerator
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


#Set parameters for model
parameters = {
    "seed" : 0,
    "population_size" : 60,
    "max_tree_depth" : 7,
    "generations" : 45,
    "tournament_window" : 7,
    "cross_mutation_prob" : [0.7, 0.3],
    "functions" : ['+','-','*','/','log','sin','cos','sqrt', '^'],
    "functions_prob" : [0.15,0.15,0.25,0.01,0.08, 0.15,0.15,0.05, 0.01],
    "dataset" : 'glass' #cancer
}
#Set seed for main execution
np.random.seed(parameters['seed'])

#Get cancer data
if parameters['dataset'] == 'cancer':
    parameters["number_of_clusters"] = 2
    df_cancer_train = pd.read_csv('data/breast_cancer_coimbra_train.csv')
    df_cancer_test = pd.read_csv('data/breast_cancer_coimbra_test.csv')
    df_train_X = df_cancer_train.drop(['Classification'], axis=1)
    df_train_Y = df_cancer_train['Classification']
    df_test_X = df_cancer_test.drop(['Classification'], axis=1)
    df_test_Y = df_cancer_test['Classification']

elif parameters['dataset'] == 'glass':
    parameters["number_of_clusters"] = 6
    df_glass_train = pd.read_csv('data/glass_train.csv')
    df_glass_test = pd.read_csv('data/glass_test.csv')
    df_train_X = df_glass_train.drop(['glass_type'], axis=1)
    df_train_Y = df_glass_train['glass_type']
    df_test_X = df_glass_test.drop(['glass_type'], axis=1)
    df_test_Y = df_glass_test['glass_type']


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
    #Going through fitness
    population_results = []
    for j in range(len(population)):
        result = FitnessCLustering(
            seed=parameters['seed'],
            k=parameters['number_of_clusters'],
            X=df_train_X,
            Y=df_train_Y,
            euclidean=False, 
            subject=population[j])
        population_results.append(result)
    #Annotating results:
    best_result = max(population_results)
    worst_result = min(population_results)
    mean_result = mean(population_results)
    generation_results[i+1] = [best_result, mean_result, worst_result]
    #Creating new population:
    champions = elitistTournament(
                    window=parameters['tournament_window'],
                    population=population,
                    results=population_results)
    population = newPopulationGenerator(
                    winners_subjects=champions,
                    population_size=parameters['population_size'],
                    cross_mutation_prob=parameters['cross_mutation_prob'],
                    max_tree_depth=parameters['max_tree_depth'])           

#Get Best Function and his performance on test
population_results = []
for j in range(len(champions)):
    result = FitnessCLustering(
        seed=parameters['seed'],
        k=parameters['number_of_clusters'],
        X=df_test_X,
        Y=df_test_Y,
        euclidean=False, 
        subject=champions[j])
    population_results.append(result)

final_subject = elitistTournament(
            window=1,
            population=champions,
            results=population_results)[0]

print("Pontuação no Teste do indivíduo vencedor:  ", max(population_results))
print("Função do indivíduo vencedor:")
final_subject.printFunction(['x','y','z'])
print()

json.dump( generation_results, open( "training_v-score.json", 'w' ) )