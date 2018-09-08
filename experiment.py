


from simulation import Simulation
import numpy as np



class Experiment():


	def __init__(self,simulation_kwargs,altruism_activated,sample_size,simulation_step,studied_function):
		self.altruism_activated = altruism_activated
		self.simulation_kwargs = simulation_kwargs
		self.sample_size = sample_size
		self.simulation_step = simulation_step
		self.studied_function = studied_function
		self.result = []



	def run(self):
		for i in range(self.sample_size):
			s = Simulation(kwargs=self.simulation_kwargs,altruism_activated=self.altruism_activated)
			for j in range(self.simulation_step):
				s.run()
			s.step()
			self.result.append(self.studied_function(s))
			
		
	def get_mean(self):
		return np.mean(self.result)

	def get_var(self):
		return np.var(self.result)


	def get_confidence_interval(self):
		if len(self.result) >= 30:
			a = 1.96*self.get_var()/np.sqrt(len(self.result))
			return (self.get_mean()-a,self.get_mean()+a)

	
