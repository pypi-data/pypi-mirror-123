import random #{temporary random}
import numpy as np


class Genetics:
	chromosome_length = 0
	population_size = 0
	search_space = ()
	chromosome_matrix = []
	pair_list = []
	data_type = 0


	def __init__(self,chromosome_length, population_size, search_space, data_type):
		self.chromosome_length = chromosome_length
		self.population_size = population_size
		self.search_space = search_space
		self.data_type = data_type


	def crossover(self, crossover_rate):
		# print(self.pair_list)
		temp_chromosome_matrix = []
		for i in range(self.population_size):
			temp_chromosome_vector = []
			for j in range(self.chromosome_length):
				rand = random.random()
				if rand < crossover_rate:
					temp_chromosome_vector.append(
					self.chromosome_matrix[self.pair_list[i][0]][j])
				else:
					temp_chromosome_vector.append(
					self.chromosome_matrix[self.pair_list[i][1]][j])
			temp_chromosome_matrix.append(temp_chromosome_vector)
		self.chromosome_matrix = np.array(temp_chromosome_matrix,int)


	# def crossoverSplice(self, crossover_rate):
	# 	temp_chromosome_matrix = []
	# 	partition = crossover_rate * self.chromosome_length
	#
	# 	for i in range(self.population_size):
	# 		temp_chromosome_vector = []
	# 		pass
	# 	pass


	def select(self, fitness_vector):
		fitness_vector_sum = fitness_vector.sum()
		self.pair_list=[]
		fitness_prob = []
		if fitness_vector_sum == 0:
			temp_fitness_prob = []
			for i in range(self.population_size):
				temp_fitness_prob.append(1/self.population_size)
			fitness_prob = np.array(temp_fitness_prob,float)
		else:
			temp_fitness_prob = []
			for i in range(self.population_size):
				temp_fitness_prob.append(fitness_vector[i]/fitness_vector_sum)
			fitness_prob = np.array(temp_fitness_prob,float)
		# print("DEBUG!")
		# print("the fitness vector probability: {}".format(fitness_prob))
		for i in range(self.population_size):
			# print("DEBUG! {}".format(i))
			rand = random.random()
			j = 0
			while rand > 0:
				rand -= fitness_prob[j]
				j += 1
			if j != 0:
				j -= 1
			rand = random.random()
			k = 0
			while rand > 0:
				rand -= fitness_prob[k]
				k += 1
			if k != 0:
				k -= 1
			self.pair_list.append((j,k))
		# print(self.pair_list)


	def populate(self):
		temp_chromosome_matrix = []
		for i in range(self.population_size):
			temp=[]
			for j in range(self.chromosome_length):
				if self.data_type == int:
					rand = random.randint(self.search_space[0],
					self.search_space[1])
				if self.data_type == float:
					rand = random.uniform(self.search_space[0],
					self.search_space[1])
				temp.append(rand)
			temp_chromosome_matrix.append(temp)
		self.chromosome_matrix = np.array(temp_chromosome_matrix,self.data_type)


	def mutate(self,mutation_rate):
		for i in range(self.population_size):
			mutant=self.chromosome_matrix[i]
			for j in range(self.chromosome_length):
				rand=random.random()
				if rand < mutation_rate:
					if self.data_type == float:
						mutant[j] = random.uniform(self.search_space[0],
						self.search_space[1])
					if self.data_type == int:
						mutant[j]=random.randint(self.search_space[0],
						self.search_space[1])
		# print(self.chromosome_matrix)


	def evolve(self,fitness_vector, mutation_rate, crossover_rate):
		self.select(fitness_vector)
		self.crossover(crossover_rate)
		self.mutate(mutation_rate)


	def setSearchSpace(self,search_space):
		self.search_space = search_space


	def setChromosomeLength(self, chromosome_length):
		self.chromosome_length = chromosome_length


	def setPopulationSize(self,population_size):
		self.population_size = population_size


	def setChromosomeMatrix(self,chromosome_matrix):
		self.chromosome_matrix = chromosome_matrix


	def getChromosomeMatrix(self):
		return self.chromosome_matrix


	def getSearchSpace(self):
		return self.search_space
