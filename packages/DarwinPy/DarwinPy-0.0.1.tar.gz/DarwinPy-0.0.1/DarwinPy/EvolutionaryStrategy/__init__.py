import random #{temporary random}
import numpy as np


class EvolutionaryStrategy:
	vector_length = 0
	search_space = ()
	parent_matrix = []
	children_matrix = []
	parent_population_size = 0
	children_population_size = 0
	data_type = 0

	def __init__(self,vector_length,parent_population_size,children_population_size,search_space,data_type):
	    self.vector_length = vector_length
	    self.search_space = search_space
	    self.parent_population_size = parent_population_size
	    self.children_population_size = children_population_size; self.data_type = data_type


	def generateParent(self):
		parent_matrix = np.array(
		range(self.vector_length * self.parent_population_size), self.data_type).reshape(
		self.parent_population_size, self.vector_length
		)
		for i in range(self.parent_population_size):
			temp = []
			for j in range(self.vector_length):
				rand = random.randint(self.search_space[0],
				self.search_space[1])
				parent_matrix[i][j] = rand
		self.parent_matrix = parent_matrix


	def generateOffspring(self, mutation_rate, parent_fitness):
		children_matrix = np.array(
		range(self.vector_length * self.children_population_size), self.data_type).reshape(
		self.children_population_size, self.vector_length
		)
		for i in range(self.children_population_size):
			children_matrix[i] = self.mutate(self.selectParent(parent_fitness),mutation_rate)
		self.children_matrix = children_matrix


	# def generateOffspring(self, parent_fitness, mutation_rate):
	# 	pass


	def mutate(self,vector, mutation_rate):
		mutant = vector.copy()
		for i in range(len(vector)):
			rand = random.random()
			if rand < mutation_rate:
				if self.data_type == float:
					mutant[i] = random.uniform(self.search_space[0],
					self.search_space[1])
				elif self.data_type == int:
					mutant[i] = random.randint(self.search_space[0],
					self.search_space[1])
		return mutant


	def selectParent(self,parent_fitness):
		fitness_vector_sum = parent_fitness.sum()
		parent_fitness_prob = parent_fitness.copy()
		if fitness_vector_sum == 0:
			for i in range(len(parent_fitness)):
				parent_fitness_prob[i] = 1/len(parent_fitness)
		else:
			for i in range(len(parent_fitness)):
				parent_fitness_prob[i] = parent_fitness[i]/fitness_vector_sum
		rand = random.random()
		j = 0
		while rand > 0:
			rand -= parent_fitness_prob[j]
			j += 1
		if j == 0:
			return self.parent_matrix[0]
		else:
			j -= 1
			return self.parent_matrix[j]


	def  evaluateParent(self,fitness_vector):
		pass


	def getFitness(self):
		pass


	def evaluateChildren(self,fitness_vector):
		pass


	def selectNextGeneration(self,parent_fitness,children_fitness):
		temp_1 = [[0]*self.vector_length]*(self.children_population_size +
		self.parent_population_size)
		temp_2 = [0]*(self.children_population_size + self.parent_population_size)
		parent_children_matrix = np.array(temp_1,int)
		parent_children_fitness = np.array(temp_2,float)

		# print("DEBUG!\nchildren matrix:\n {}\nparent_matrix:\n {}\n".
		# format(self.children_matrix,self.parent_matrix))
		for i in range(self.parent_population_size):
			parent_children_matrix[i] = self.parent_matrix[i]

		j = 0
		for i in range(self.parent_population_size, self.parent_population_size + self.children_population_size):
			parent_children_matrix[i] = self.children_matrix[j]
			j += 1

		for i in range(self.parent_population_size):
			parent_children_fitness[i] = parent_fitness[i]
		j = 0
		for i in range(self.parent_population_size, self.parent_population_size + self.children_population_size):
			# print("DEBUG!")
			parent_children_fitness[i] = children_fitness[j]
			j += 1

		fitness_prob = np.array([0]*(self.parent_population_size + self.children_population_size),
		float)

		fitness_vector_sum = parent_children_fitness.sum()
		if fitness_vector_sum == 0:
			for i in range(self.parent_population_size + self.children_population_size):
				fitness_prob[i] = 1/self.parent_children_fitness
		else:
			for i in range(self.parent_population_size + self.children_population_size):
				fitness_prob[i] = parent_children_fitness[i]/fitness_vector_sum

		temp_3 = [[0]*self.vector_length]*self.parent_population_size
		# print("the fitness probability vector: {}".format(fitness_prob))
		next_generation = np.array(temp_3, self.data_type)
		for i in range(self.parent_population_size):
			rand = random.random()
			j = 0
			while rand > 0:
				rand -= fitness_prob[j]
				j += 1
			if j != 0:
				j -= 1

			next_generation[i] = parent_children_matrix[j]
		self.parent_matrix = next_generation

		# print("parent-children matrix:\n {}".
		# format(parent_children_matrix))


	def evolve(self,children_fitness,parent_fitness):
		self.selectNextGeneration(children_fitness,parent_fitness)


	def getParentGeneration(self):
		return self.parent_matrix


	def getChildrenGeneration(self):
		return self.children_matrix
