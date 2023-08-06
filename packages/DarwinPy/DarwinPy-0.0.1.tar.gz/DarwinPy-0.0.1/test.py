import DarwinPy
import numpy as np

def hammingDist(goal, matrix):
    result = []
    for i in range(len(matrix)):
        temp = 0.
        for j in range(len(goal)):
            if goal[j] == matrix[i][j]:
                temp += 1.
        result.append(temp)
    return result


if __name__ == "__main__":
    mouse_population = 5
    mutation_rate = 0.5
    search_space = (0,1)
    goal = np.array([1,0,1,1,0,1,1, 0,1,1,0],int)
    chromosome_length = len(goal)

    mouse_species = DarwinPy.Genetics.Genetics(chromosome_length,
    mouse_population, (0,1), int)
    print("mouse species instantiated:\n {}".format(mouse_species))

    print("the goal:\n {}".format(goal))

    mouse_species.populate()
    print("get mouse matrix(GA):\n {}".
    format(mouse_species.getChromosomeMatrix()))


    fitness_vector = np.array(
    hammingDist(goal,mouse_species.getChromosomeMatrix()),
    float)

    print("get fitness vector: {}".format(fitness_vector))

    is_goal = False
    gen = 1
    while is_goal == False:
        print("Generation #{}\n".format(gen))
        gen += 1
        mouse_species.evolve(fitness_vector,
        mutation_rate, 0.5)
        print("get mouse matrix(GA):\n {}".
        format(mouse_species.getChromosomeMatrix()))
        fitness_vector = np.array(
        hammingDist(goal,mouse_species.getChromosomeMatrix()),
        float)

        print("get fitness vector: {}".format(fitness_vector))
        if chromosome_length in fitness_vector:
            is_goal = True
