


from person import Person
from random import randint



class Group():



	def __init__(self,food_cost,genetic_proportion,advantage,lifespan,initial_group_size=0):
		self.persons = []
		self.food_cost = food_cost
		self.advantage=advantage
		self.lifespan = lifespan
		for i in range(initial_group_size):
			genom = {}
			for gene in genetic_proportion.keys():
				randd = randint(1,100)
				genom[gene] = (randd<(100*genetic_proportion[gene]))
			self.persons.append(self.create_person(genom))


	def create_person(self,genom):
		person = Person(genom,self.advantage)
		return(person)


	def altruism(self):
		self.persons.sort(key=lambda x:x.food)
		for p in self.persons[::-1]:
			if p.food > self.food_cost and p.genom["altruism"]:
				for p2 in self.persons[::-1]:
					if p2.food < self.food_cost:
						p2.food += p.food - self.food_cost
						p.food -= self.food_cost			 

	def age_persons(self):
		for person in self.persons:
			person.age += 1

	def kill_weaks(self,food_cost):
		self.age_persons()
		index = []
		for i in range(len(self.persons)):
			person = self.persons[i]
			person.food -= food_cost
			if person.food < 0 or person.age >= self.lifespan:
				index.append(i)
		for i in index[::-1]:
			#print("weak killed")
			self.persons.pop(i)


	def give_birth(self):
		scale = 10000
		for i in range(len(self.persons)):
			new_born = self.persons[i].give_birth()
			if new_born is not None:
				self.persons.append(new_born)

	def get_size(self):
		return len(self.persons)

	def get_altruist_proportion(self):
		altruists = 0
		for person in self.persons:
			altruists += int(person.genom["altruism"])
		return float(altruists)/max(1,len(self.persons))
