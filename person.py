


from random import randint


class Person():

	DEFAULT_GENOTYPE = {
			"altruism":False, #Will share food if have more than needed
			"advantage":False #Advantage on gathering food
	}


	def __init__(self,**kwargs):
		self.food = 0
		self.altruism = altruism
		self.genetype= self.DEFAULT_GENOTYPE
		for key in **kwargs:
			self.genotype[key]=True


	def new_score(self):
		self.score = randint(1,100)


	def get_score(self):
		return self.score

	def receive_food(self,total,food):
		self.food += food*float(self.score)/total
