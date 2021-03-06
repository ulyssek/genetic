





from setings import default_kwargs
from group import Group
from logger import Logger
from timeit import time
from tools import hat_function







class Simulation():


	LOGGING_FUNCTIONS={
		"group_number" 		: lambda self : sum(map(lambda x : len(x.persons)>0,self.groups)),
		"person_number" 	: lambda self : sum(map(lambda x : len(x.persons),self.groups)),
		"altruist_proportion"	: lambda self : self.total_person_proportion("altruism"),
		"advantage_proportion"	: lambda self : self.total_person_proportion("advantage"),
		"alternative_gene_rate_proportion": lambda self : self.total_person_proportion("gene_rate_alternative"),
		"temp_advantage"	: lambda self : self.compute_advantage_reference(),
		"average_mutation_rate" : lambda self : self.get_average_gene_rate("mutation"),
		"average_inner_rate" 	: lambda self : self.get_average_gene_rate("innervalue"),
		"average_lifespan"	: lambda self : self.get_average_gene_rate("lifespan"),
		"average_birth_rate"	: lambda self : self.get_average_gene_rate("birth_rate"),
	}



	def __init__(self,kwargs=default_kwargs,logging_keys=[]):
		for key in kwargs.keys():
			self.__setattr__(key,kwargs[key])
		self.current_step = 0
		self.groups = []
		for i in range(self.initial_group):
			self.groups.append(self.create_group())
		try:
			self.take_over_key
			self.take_over_activated = True
			self.take_over_step = None
		except AttributeError:
			self.take_over_activated = False
		self.altruism_activated = ("altruism" in kwargs["genetic_proportion"].keys())
		self.logging_keys = logging_keys
		self.logging_activated = (logging_keys != [])
		self.logger = Logger(self,logging_keys)
		#self.run = self.build_running_function()

	"""
	def build_running_function(self):
		if self.altruism_activated and self.logging_keys != []:
			def run():
				for i in range(self.season_number):
					self.step()
				self.kill_weaks()
				self.give_birth()
				self.split_group()
				if self.altruism_activated:
					self.altruism()
				self.log()
		elif self.altruism_activated:
			def run():
				for i in range(self.season_number):
					self.step()
				self.kill_weaks()
				self.give_birth()
				self.split_group()
				if self.altruism_activated:
					self.altruism()
		elif self.logging_keys != []:
			def run():
				for i in range(self.season_number):
					self.step()
				self.kill_weaks()
				self.give_birth()
				self.split_group()
				self.log()
		else:
			def run():
				for i in range(self.season_number):
					self.step()
				self.kill_weaks()
				self.give_birth()
				self.split_group()

		return run
	"""

	def run(self):
		self.advantage_reference = self.compute_advantage_reference()
		self.advantage_function = self.compute_advantage_function(self.compute_score_function)
		for i in range(self.season_number):
			self.step()
		self.kill_weaks()
		self.give_birth()
		self.split_group()
		if self.altruism_activated:
			self.altruism()
		if self.logging_activated:
			self.log()
		if self.take_over_activated:
			self.take_over()
		self.current_step += 1

	def compute_advantage_reference(self):
		k = self.advantage_reference_frequency
		i = self.current_step
		return self.advantage_reference_amplitude*(k/2+(k*1.5-(((k*2)-i%(k*2))+(i%k)))/(k/2)*((k/2)-(i%k)))/self.advantage_reference_frequency+self.advantage_reference_base
		

	def take_over(self):
		if self.total_person_proportion(self.take_over_key) == 1:
			self.take_over_step = self.current_step
			self.take_over_activated = False

	def get_take_over_step(self):
		return self.take_over_step
		

	def log(self):
		values = list(map(lambda x : self.LOGGING_FUNCTIONS[x](self),self.logging_keys))
		self.logger.log(values)

	def create_group(self,group_size=None):
		if group_size is None:
			group_size=self.initial_group_size
		group = Group(
			self.food_cost,
			self.genetic_proportion,
			self.person_attribute,
			group_size,
		)
		return group
	

	def altruism(self):
		for group in self.groups:
			group.altruism()

	def total_person_proportion(self,gene):
		positive=0
		negative=0
		for group in self.groups:
			for person in group.persons:
				positive += int(person.genom[gene])
				negative += 1-int(person.genom[gene])
		return float(positive)/max(1,(positive+negative))

	def get_average_gene_rate(self,gene):
		current_sum = 0
		current_count = 0
		for group in self.groups:
			for person in group.persons:
				current_sum += person.get_rate_from_gene(gene)
				current_count += 1
		return float(current_sum)/max(1,current_count)

	def split_group(self):
		for group in self.groups:
			if group.get_size() > self.group_size:
				last_group = self.create_group(0)
				self.groups.append(last_group)
				last_group.persons = group.persons[:int(self.group_size/2):]
				group.persons = group.persons[int(self.group_size/2)::]

	def kill_weaks(self):
		for group in self.groups:
			group.kill_weaks(self.food_cost)

	def give_birth(self):
		for group in self.groups:
			group.give_birth()

	def step(self):
		total = self.collect_total()
		self.give_food(total)

	def collect_total(self):
		total_score = 0
		for group in self.groups:
			for person in group.persons:
				total_score += person.new_score(self.advantage_function)
		return total_score


	def give_food(self,total_score):
		food_ratio = self.food_per_season/max(1,total_score)
		for group in self.groups:
			for person in group.persons:
				person.receive_food(food_ratio)

	def function_list(self,function_number):
		l = [
			lambda : self.total_person_proportion("advantage"),
			lambda : self.get_take_over_step(),
			lambda : self.get_average_gene_rate("birth_rate"),
			lambda : self.get_average_gene_rate("mutation"),
			lambda : self.total_person_proportion("gene_rate_alternative")
		]
		return l[function_number]()
	
	def compute_advantage_function(self,i):
		functions = [
			lambda x,y : hat_function(10,x,self.advantage_reference,y),
			lambda x,y : hat_function(20,50,25,y)+hat_function(1,52.5,75,y),
		]
		return functions[i]

	"""
	def compute_advantage_function(self):
		return lambda x,y : hat_function(20,50,25,y)+hat_function(1,52.5,75,y)
	"""




