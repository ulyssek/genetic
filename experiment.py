


from simulation import Simulation
import numpy as np
from logging import log

from timeit import time

from multiprocessing import Pool

from scipy.special import stdtrit
import scipy.stats as st

from math import sqrt


def do(args):
	self = args[0]
	i = args[1]
	print_progression = args[2]
	s = self.simulation_class(kwargs=self.simulation_kwargs)
	for j in range(self.simulation_step):
		s.run()
	self.result.append(s.function_list(self.studied_function))
	if print_progression:
		self.print_progression(i)
	return s.function_list(self.studied_function)

class Experiment():


	def __init__(self,kwargs):
		for key in kwargs.keys():
			self.__setattr__(key,kwargs[key])
		self.result = []

	def run(self):
		self.progression = 0
		self.starting_time = time.time()
		if self.sample_size==None:
			self.compute_sample_size()
		print("Launching experiment, sample size : %s, step number : %s" % (self.sample_size,self.simulation_step))
		l = []
		for i in range(self.exploration_size,self.sample_size):
			l.append((self,i,True))
		pool = Pool()
		self.result = pool.map(do,l)
		pool.close()
		pool.join()
		print("Computation over")

	def compute_sample_size(self):
		print("Computing sample size")
		t = st.norm.ppf(self.alpha/2)
		m = self.interval_lenght
		for i in range(self.exploration_size):
			do((self,i,False))
		var = np.var(self.result)
		self.sample_size = int(var*pow(t,2)/pow(m,2))
		print("Sample size computed : %s" % (self.sample_size,))
		

	def print_progression(self,i):
		if ((i+1) % max(1,int(self.sample_size/10)) == 0):
			self.temp_time = time.time()
			exec_time = self.temp_time - self.starting_time
			rounded_time = int(exec_time*10)/float(10)
			print("%s percent of the simulation done (%s simulations), exec time : %s seconds" % (int(float(i+1)/self.sample_size*100),i+1,rounded_time))
			self.starting_time = self.temp_time

	def get_mean(self):
		return np.mean(self.result)

	def get_var(self):
		return np.var(self.result)


	def get_confidence_interval(self,alpha=0.05):
		#if len(self.result) >= 30:
		n = self.sample_size
		tvalue = stdtrit(n,1-alpha)
		mu = self.get_mean()
		s = sqrt(self.get_var())
		return (mu - tvalue*s/sqrt(n),mu + tvalue*s/sqrt(n))
		"""
		else:
			print("Not enough data")
		"""

	
	def get_proportion_confidence_interval(self,alpha=0.05):
		temp_result = list(map(lambda x : int(x is not None),self.result))
		n = len(temp_result)
		p = sum(temp_result)/len(temp_result)
		z=st.norm.ppf(alpha/2)
		se = sqrt(p*(1-p)/n)
		if p*n < 15 or (n-p*n)<15:
			print("Not enough data")
			return
		return (p-z*se,p+z*se)	



