


from person import Person
from random import randint



class Group():



	def __init__(self,food_cost,initial_group_size=0,altruist_proportion=0):
		self.persons = []
		self.food_cost = food_cost
		self.altruist_proportion = altruist_proportion
		for i in range(initial_group_size):
			self.persons.append(Person(randint(1,100)<(altruist_proportion*100)))



	def altruism(self):
		self.persons.sort(key=lambda x:x.food)
		for p in self.persons[::-1]:
			if p.food > self.food_cost and p.altruism:
				for p2 in self.persons[::-1]:
					if p2.food < self.food_cost:
						p2.food += p.food - self.food_cost
						p.food -= self.food_cost			 

	def kill_weaks(self,food_cost):
		index = []
		for i in range(len(self.persons)):
			person = self.persons[i]
			person.food -= food_cost
			if person.food < 0:
				index.append(i)
		for i in index[::-1]:
			#print("weak killed")
			self.persons.pop(i)


	def give_birth(self,birth_rate):
		scale = 10000
		for person in self.persons:
			if randint(1,scale)< birth_rate*scale:
				#print("new_birth")
				self.persons.append(Person(person.altruism))

	def get_size(self):
		return len(self.persons)

	def get_altruist_proportion(self):
		altruists = 0
		for person in self.persons:
			altruists += int(person.altruism)
		return float(altruists)/max(1,len(self.persons))
