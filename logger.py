


import pandas as pd



class Logger():


	def __init__(self,object,columns=[]):
		self.object = object
		self.columns = columns
		self.step = 0
		keys = {}
		for column in columns:
			keys[column]=[]
		self.logs = pd.DataFrame(columns=keys)



	def log(self,values):
		self.step += 1
		self.logs.loc[self.step] = values

	def save_in_file(self,file_name):
		pass
		
		
