import numpy

def createFitnessProbVector(fitness_vector):
    fitness_vector_sum = fitness_vector.sum()
    fitness_prob = fitness_vector.copy()
    if fitness_vector_sum == 0:
        for i in range(len(fitness_vector)):
            fitness_prob[i] = 1/len(fitness_vector)
    else:
        for i in range(len(fitness_vector)):
            fitness_prob[i] = fitness_vector[i]/fitness_vector_sum[i]
    return fitness_prob
