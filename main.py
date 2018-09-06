



from simulation import Simulation



alt = []


for j in range(2):
	s = Simulation(altruism_activated=False)


	for i in range(0):
		s.run()
	s.step()
	alt.append(s.total_altruist_proportion())



print(sum(alt)/float(len(alt)))



