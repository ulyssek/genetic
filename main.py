



from simulation import Simulation



alt = []


for j in range(10):
	s = Simulation(altruism_activated=True)


	for i in range(10):
		s.run()
	s.step()
	alt.append(s.total_altruist_proportion())



print(sum(alt)/float(len(alt)))



