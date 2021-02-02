def elitistTournament(window, population, results):
    zipped = zip(results, population)
    sorted_zip = sorted(zipped)
    sorted_population = [x for _,x in sorted_zip]
    champions = sorted_population[(-1*window):]
    return champions
    
