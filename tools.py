



def add_gene_to_genom(genom,gene,number):
	for i in range(number):
		genom[gene+str(i)]=0


def kinda_hat_function(a,b,c,x):
	return b*x/a+b*(a-c)/a

def hat_function(a,b,c,x):
	return max(0,min(kinda_hat_function(a,b,c,x),kinda_hat_function(-a,b,c,x)))	
