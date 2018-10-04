


from random import randint
from tools import hat_function


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
		"innervalue0":False,
		"innervalue1":False,
		"innervalue2":False,
		"innervalue3":False,
		"innervalue4":False,
		"innervalue5":False,
		"innervalue6":False,
	}


	def __init__(self,genom,kwargs):
		for key in kwargs.keys():
			self.__setattr__(key,kwargs[key])
		self.food = 0
		self.age = 0
		self.genom= dict(self.DEFAULT_GENOTYPE)
		if type(genom) == type([]):
			for key in genom:
				self.genom[key]=True
		else:
			self.genom = genom
		self.gene_rate = {}
		self.get_rate_from_gene = self.get_rate_from_gene_1
		try:
			if self.genom["gene_rate_alternative"]:
				self.gene_rate_from_gene = self.gene_rate_from_gene_2
		except:
			pass		
		self.gene_rate["mutation"] 	= self.get_rate_from_gene("mutation") 
		self.gene_rate["innervalue"] 	= self.get_rate_from_gene("innervalue")
		self.gene_rate["lifespan"]	= self.lifespan_scale*(self.get_rate_from_gene("lifespan")+1)
		self.gene_rate["birth_rate"]	= self.birth_rate_scale/max(1,self.get_rate_from_gene("birth_rate"))
		try:
			self.advantage = bool(self.genom["advantage"])
		except KeyError:
			self.advantage = False


	def compute_advantage_score(self,advantage_reference):
		return int(self.advantage)*hat_function(10,self.advantage_scale,advantage_reference,self.gene_rate["innervalue"])

	def new_score(self,advantage_reference):
		self.score = randint(1,100)+self.compute_advantage_score(advantage_reference)
		return self.score

	def give_birth(self):
		if randint(1,100)< self.gene_rate["birth_rate"] and self.food > self.child_cost:
			self.food -= self.child_cost
			new_genom = {}
			for gene in self.genom:
				new_genom[gene] = self.genom[gene]!=(randint(1,99)<=self.gene_rate["mutation"])
			return self.create_person(new_genom) 
		

	def create_person(self,genom):
		person_kwargs = {
			#"birth_rate":self.birth_rate,
			"advantage_scale":self.advantage_scale,
			"lifespan_scale":self.lifespan_scale,
			"child_cost":self.child_cost,
			"birth_rate_scale":self.birth_rate_scale,
		}
		return Person(genom,person_kwargs)

	def get_score(self):
		return self.score

	def get_genom_keys(self):
		genom_keys = []
		for gene in self.genom.keys():
			if self.genom[gene]:
				genom_keys.append(gene)
		return genom_keys

	def receive_food(self,food_ratio):
		self.food += food_ratio*self.score

	def aged(self):
		self.age += 1

	def get_rate_from_gene_1(self,gene_name):
		if gene_name in self.gene_rate.keys():
			return self.gene_rate[gene_name]
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
		return float(rate)/pow(2,power+1)*100


	def get_rate_from_gene_2(self,gene_name):
		if gene_name in self.gene_rate.keys():
			return self.gene_rate[gene_name]
		rate = 0
		power = 0
		for key in self.genom.keys():
			a = key.split(gene_name)
			if len(a)==2 and a[0]=='':
				try:
					rate+=int(self.genom[key])
					power+=1
				except:
					pass
		return 100.*rate/max(1,power)
