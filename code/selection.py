import numpy as np
def elitistTournament(window, population, results):
    population = np.array(population)
    results = np.array(results)
    inds = results.argsort()
    champions = population[inds][::-1][:window]
    return champions
        
