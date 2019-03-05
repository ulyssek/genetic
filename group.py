


from person import Person
from random import randint,shuffle



class Group():



	def __init__(self,food_cost,genetic_proportion,person_attribute,initial_group_size=0):
		self.persons = []
		self.person_attribute=person_attribute
		self.food_cost = food_cost
		for i in range(initial_group_size):
			genom = {}
			for gene in genetic_proportion.keys():
				randd = randint(1,100)
				genom[gene] = (randd<(100*genetic_proportion[gene]))
			self.persons.append(self.create_person(genom))


	def create_person(self,genom):
		person = Person(genom,self.person_attribute)#self.birth_rate,self.advantage_scale,self.lifespan_scale,child_cost)
		return(person)


	def altruism(self):
		self.persons.sort(key=lambda x:x.food)
		for p in self.persons[::-1]:
			if p.food > self.food_cost and p.genom["altruism"]:
				for p2 in self.persons[::-1]:
					if p2.food < self.food_cost:
						p2.food += p.food - self.food_cost
						p.food -= self.food_cost			 

	def kill_weaks(self,food_cost):
		index = []
		for i in range(len(self.persons)):
			self.persons[i].aged()
			self.persons[i].food -= food_cost
			if self.persons[i].food < 0 or self.persons[i].age >= self.persons[i].gene_rate["lifespan"]:
				index.append(i)
		for i in index[::-1]:
			self.persons.pop(i)


	def give_birth(self):
		for i in range(len(self.persons)):
			new_born = self.persons[i].give_birth()
			if new_born is not None:
				self.persons.append(new_born)

	def get_size(self):
		return len(self.persons)

	def sexual_reproduction(self):
		reproducer = []
		for i in range(len(self.persons)):
			if self.persons[i].want_to_give_birth():
				reproducer.append(persons[i])
		shuffle(reproducer)
		
		






