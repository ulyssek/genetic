





from setings import default_kwargs
from group import Group
from logger import Logger






class Simulation():



	def __init__(self,kwargs=default_kwargs,altruism_activated=False):
		for key in kwargs.keys():
			self.__setattr__(key,kwargs[key])
		self.groups = []
		for i in range(self.initial_group):
			self.groups.append(Group(self.food_cost,self.initial_group_size,self.altruist_proportion))
		self.altruism_activated = altruism_activated
		logging_keys = [
			"group_number",
			"person_number",
			"altruist_proportion",
			]
		self.logger = Logger(self,logging_keys)

	def run(self):
		"""
		print("#####")
		print("running")
		"""
		for i in range(self.season_number):
			self.step()
		self.kill_weaks()
		self.give_birth()
		self.split_group()
		if self.altruism_activated:
			self.altruism()
		#print(self.total_altruist_proportion())
		self.log()

	def log(self):
		group_number = sum(map(lambda x : len(x.persons)>0,self.groups))
		person_number = sum(map(lambda x : len(x.persons),self.groups))
		altruist_proportion = self.total_altruist_proportion()
		values = [group_number,person_number,altruist_proportion]
		self.logger.log(values)


	def altruism(self):
		for group in self.groups:
			group.altruism()

	def total_altruist_proportion(self):
		altruists = 0
		selfish = 0
		for group in self.groups:
			for person in group.persons:
				altruists += int(person.altruism)
				selfish += 1-int(person.altruism)

		return float(altruists)/(altruists+selfish)

	def split_group(self):
		for group in self.groups:
			if group.get_size() > self.group_size:
				self.groups.append(Group(self.food_cost,0,self.altruist_proportion))
				last_group = self.groups[-1]
				last_group.persons = group.persons[:int(self.group_size/2):]
				group.persons = group.persons[int(self.group_size/2)::]

	def kill_weaks(self):
		for group in self.groups:
			group.kill_weaks(self.food_cost)

	def give_birth(self):
		for group in self.groups:
			group.give_birth(self.birth_rate)

	def step(self):
		total = self.collect_total()
		self.give_food(total)


	def count_persons(self):
		print(str(len(self.groups))+' groups')
		for i,group in enumerate(self.groups):
			print('group ' + str(i) + ' : ' + str(len(group.persons)))
			print('altruists proportion : ' + str(group.get_altruist_proportion()))
		print('altruist proportion : ' + str(self.total_altruist_proportion()))
		

	def collect_total(self):
		total_score = 0
		for group in self.groups:
			for person in group.persons:
				person.new_score()
				total_score += person.get_score()
		return total_score


	def give_food(self,total_food):
		for group in self.groups:
			for person in group.persons:
				person.receive_food(total_food,self.food_per_season)

