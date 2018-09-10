


from simulation import Simulation
import numpy as np
from logging import log

from timeit import time



class Experiment():


	def __init__(self,simulation_class,simulation_kwargs,sample_size,simulation_step,studied_function):
		self.simulation_class = simulation_class
		self.simulation_kwargs = simulation_kwargs
		self.sample_size = sample_size
		self.simulation_step = simulation_step
		self.studied_function = studied_function
		self.result = []



	def run(self):
		print("Launching experiment, sample size : %s, step number : %s" % (self.sample_size,self.simulation_step))
		last_signal = 0
		starting_time = time.time()
		for i in range(self.sample_size):
			s = self.simulation_class(kwargs=self.simulation_kwargs)
			for j in range(self.simulation_step):
				s.run()
			self.result.append(self.studied_function(s))
			if ((i+1) % int(self.sample_size/10) == 0) and (self.sample_size/5 > last_signal):
				temp_time = time.time()
				exec_time = temp_time - starting_time
				rounded_time = int(exec_time*10)/float(10)
				print("%s percent of the simulation done (%s simulations), exec time : %s seconds" % (int(float(i+1)/self.sample_size*100),i+1,rounded_time))
				starting_time = temp_time
		print("Computation over")

			
		
	def get_mean(self):
		return np.mean(self.result)

	def get_var(self):
		return np.var(self.result)


	def get_confidence_interval(self):
		if len(self.result) >= 30:
			a = 1.96*self.get_var()/np.sqrt(len(self.result))
			return (self.get_mean()-a,self.get_mean()+a)

	
