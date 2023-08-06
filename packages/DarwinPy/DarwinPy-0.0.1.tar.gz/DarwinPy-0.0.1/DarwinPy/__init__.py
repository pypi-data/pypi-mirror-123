import DarwinPy.Genetics
import DarwinPy.EvolutionaryStrategy
import multiprocessing as mp
import DarwinPy.Utils as utils
import numpy


# class DarwinPyCore:
#     number_of_processes = 0
#     object_id = ""
#     population = []
#     core_type = ["Genetics"]
#
#     def __init__(self, number_of_processes, object_id):
#         if not object_id in self.core_type:
#             raise TypeError(utils.error['E0002'])
#         else:
#             self.number_of_processes = number_of_processes
#             self.object_id = object_id
#
#
#     def initializeGenetics(self,chromosome_length, population_size, search_space, data_type):
#         if  self.object_id != "Genetics":
#             raise TypeError(f"{utils.error['E0001']}")
#         else:
#             temp = []
#             for _ in range(self.number_of_processes):
#                 temp.append(DarwinPy.Genetics.Genetics(
#                 chromosome_length, population_size, search_space, data_type
#                 ))
#             for cluster in temp:
#                 cluster.populate()
#             self.population = temp
#
#
#
#
#     def evolve(self,fitness_matrix,mutation_rate,crossover_rate):
#         if self.object_id == "Genetics":
#             processes = [0] * self.number_of_processes
#             # crossover_processes = [0] * self.number_of_processes
#             # mutation_processes = [0] * self.number_of_processes
#
#             for i in range(self.number_of_processes):
#                 # print("Debug")
#                 # print(fitness_matrix[i])
#                 # print(self.population[i].select)
#                 # self.population[i].select(fitness_matrix[i])
#                 processes[i] = mp.Process(target = self.population[i].evolve,
#                 args = [fitness_matrix[i],mutation_rate,crossover_rate])
#                 # crossover_processes[i] = mp.Process(target = self.population[i].crossover,
#                 # args = [crossover_rate])
#                 # mutation_processes[i] = mp.Process(target = self.population[i].mutate,
#                 # args = [mutation_rate])
#
#             for process in processes:
#                 process.start()
#
#             for process in processes:
#                 process.join()
#
#             # print(f"Done number of selection processes completed {len(processes)}")
#
#             print("Debug...")
#             # for i in range(self.number_of_processes):
#             #
#             # for crossover_process in crossover_processes:
#             #     crossover_process.start()
#
#             # for crossover_process in crossover_processes:
#             #     crossover_process.join()
#             #
#             # for mutation_process in mutation_processes:
#             #     mutation_process.start()
#             #
#             # for mutation_process in mutation_processes:
#             #     mutation_process.join()
#
#
#     def getChromosomeMatrixList(self):
#         result = []
#         for i in range(self.number_of_processes):
#             result.append(self.population[i].getChromosomeMatrix())
#         return numpy.array(result,float)
