import numpy as np

def flatten(input):
	output=[]
	for ls in input:
		if isinstance(ls,list):
			for x in ls:
				output.append(x)
		else:
			output.append(ls)
	return output

outmol={'pCof':{'num':['pCof'],'denom':['Cof','Cofactin']},
        'actCof':{'num':['Cof','Cofactin'],'denom':[]},
        'pLIMK':{'num':['pLIMK','pLIMKCof'],'denom':[]},
        'SSH':{'num':['SSH','SCappSSH'],'denom':[]},
        'actRac':{'num':['RacPAK','RacPAKLIMK','RacPAKSSH'],'denom':[]},
        'CKtot':{'num':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4'],'denom':[]},
        'PKA_PAK':{'num':['pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi','pLIMK','pLIMKCof'],'denom':[]}} #molecule(s) to save as representative of change in basal.  
all_mols=np.unique(flatten([list(k['num'])+list(k['denom']) for k in outmol.values()]))

#outmol={'pCof':['Cof','Cofactin']} #Each key is numerator, each value is denominator, which can be empty list
#all_mols=flatten(list(outmol.keys())+list(outmol.values()))
