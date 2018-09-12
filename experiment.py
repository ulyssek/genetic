


from simulation import Simulation
import numpy as np
from logging import log

from timeit import time

from multiprocessing import Pool



def do(args):
	self = args[0]
	i = args[1]
	s = self.simulation_class(kwargs=self.simulation_kwargs)
	for j in range(self.simulation_step):
		s.run()
	self.result.append(s.function_list(self.studied_function))
	self.print_progression(i)
	return s.function_list(self.studied_function)

class Experiment():


	def __init__(self,simulation_class,simulation_kwargs,sample_size,simulation_step,studied_function):
		self.simulation_class = simulation_class
		self.simulation_kwargs = simulation_kwargs
		self.sample_size = sample_size
		self.simulation_step = simulation_step
		self.studied_function = studied_function
		self.result = []
		pass

	def run(self):
		print("Launching experiment, sample size : %s, step number : %s" % (self.sample_size,self.simulation_step))
		self.progression = 0
		self.starting_time = time.time()
		l = []
		for i in range(self.sample_size):
			l.append((self,i))
		pool = Pool()
		self.result = pool.map(do,l)
		pool.close()
		pool.join()
		print("Computation over")

	def print_progression(self,i):
		if ((i+1) % int(self.sample_size/10) == 0):
			self.temp_time = time.time()
			exec_time = self.temp_time - self.starting_time
			rounded_time = int(exec_time*10)/float(10)
			print("%s percent of the simulation done (%s simulations), exec time : %s seconds" % (int(float(i+1)/self.sample_size*100),i+1,rounded_time))
			self.starting_time = self.temp_time

	def get_mean(self):
		return np.mean(self.result)

	def get_var(self):
		return np.var(self.result)


	def get_confidence_interval(self):
		if len(self.result) >= 30:
			a = 1.96*self.get_var()/np.sqrt(len(self.result))
			return (self.get_mean()-a,self.get_mean()+a)

	
