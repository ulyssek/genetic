


from random import randint


class Person():

	DEFAULT_GENOTYPE = {
		"altruism":False, #Will share food if have more than needed
		"advantage":False, #Advantage on gathering food
		"mutation0":False,
		"mutation1":False,
		"mutation2":False,
		"mutation3":False,
		"mutation4":False,
		"mutation5":False,
		"mutation6":False,
	}


	def __init__(self,genom,birth_rate,advantage=0.01):
		self.food = 0
		self.age = 0
		self.genom= dict(self.DEFAULT_GENOTYPE)
		if type(genom) == type([]):
			for key in genom:
				self.genom[key]=True
		else:
			self.genom = genom
		self.advantage=advantage
		self.birth_rate=birth_rate
		self.mutation_rate = self.get_rate_from_gene("mutation") 


	def new_score(self):
		self.score = randint(1,100)+self.advantage*int(self.genom["advantage"])

	def give_birth(self):
		scale = 10000
		new_genom = {}
		if randint(1,scale)< self.birth_rate*scale:
			for gene in self.genom:
				new_genom[gene] = self.genom[gene]!=(randint(1,99)<=(self.mutation_rate*100))
			return self.create_person(new_genom) 
		

	def create_person(self,genom):
		return Person(genom,self.birth_rate,self.advantage)

	def get_score(self):
		return self.score

	def get_genom_keys(self):
		genom_keys = []
		for gene in self.genom.keys():
			if self.genom[gene]:
				genom_keys.append(gene)
		return genom_keys

	def receive_food(self,total,food):
		self.food += food*float(self.score)/total

	def get_rate_from_gene(self,gene_name):
		rate = 0
		power = 0 
		for key in self.genom.keys():
			a = key.split(gene_name)
			if len(a)==2 and a[0]=='':
				try:
					rate+=int(self.genom[key])*pow(2,int(a[1]))
					power=max(int(a[1]),power)
				except:
					pass
		return float(rate)/pow(2,power+1)
