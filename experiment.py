


from simulation import Simulation



class Experiment():


	def __init__(self,simulation_kwargs,altruism_activated,sample_size,simulation_step,studied_function):
		self.altruism_activated = altruism_activated
		self.simulation_kwargs = simulation_kwargs
		self.sample_size = sample_size
		self.simulation_step = simulation_step
		self.result = []



	def run(self):
		for i in range(self.sample_size):
			s = Simulation(kwargs=self.simulation_kwargs,altruism_activated=self.altruism_activated)
			for j in range(self.simulation_step):
				s.run()
			s.step()
			self.result.append(studied_function)
			
		
