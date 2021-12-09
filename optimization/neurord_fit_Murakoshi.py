#How to use :doc:`ajustador` to fit a NeuroRD model to experimental data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''This demonstration fits a single reaction model (Model_pSynGap) to data.
'''

import ajustador as aju
import numpy as np
from ajustador import drawing,loadconc,nrd_fitness
from ajustador.helpers import converge
import os

#model is the xml file that contains the neuroRD model to simulate and adjust parameters
dirname='./'  #where data and model are stored.  Multiple datafiles allowed
model_set='Model_Cof-Murakoshi'
exp_name='Murakoshi_Nature_2011' #name of data file selected from dirname; each file may contain several molecules
mol=['pKal','Cdc42GTP'] #which molecule(s) to match in optimization
tmpdir='/tmp/'+dirname+'_'+model_set.slpit('-')[-1]

# number of iterations, use 1 for testing
# default popsize=8, use 3 for testing
iterations=1
popsize=3
test_size=3#25

os.chdir(dirname)
exp=loadconc.CSV_conc_set(exp_name)

P = aju.xml.XMLParam
#list of parameters to change/optimize
params = aju.optimize.ParamSet(P('phos_fwd_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Kal+CKpCamCa4--KalCKpCamCa4"]/forwardRate'),
                               P('phos_rev_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="CKpCamCa4+Kal--KalCKpCamCa4"]/reverseRate'),
                               P('phos_kcat_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="KalCKpCamCa4--pKal+CKpCamCa4]/forwardRate'),
                               P('phos_fwd_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Kal+PKAc--KalPKAc"]/forwardRate'),
                               P('phos_rev_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Kal+PKAc--KalPKAc"]/reverseRate'),
                               P('phos_kcat_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="KalPKAc--pKal+PKAc"]/forwardRate'),
                               P('phos_fwd_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Cdc42GDP+pKal--Cdc42GDPpKal"]/forwardRate'),
                               P('phos_rev_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Cdc42GDP+pKal--Cdc42GDPpKal"]/reverseRate'),
                               P('phos_kcat_rate', 0, min=0, max=1e-12, xpath='//Reaction[@id="Cdc42GDP+pKal--Cdc42GTP+pKal"]/forwardRate'))


###################### END CUSTOMIZATION #######################################

fitness = nrd_fitness.specie_concentration_fitness(species_list=mol)

############ Test fitness function
#sim = aju.xml.NeurordSimulation('/tmp', model=model, params=params)
#cp /tmp/???/model.h5 modelname.split('.')[0]+'.h5'
#sim2=aju.xml.NeurordResult('Model_syngap_ras.h5')
#print(fitness(sim2, exp))
################

fit = aju.optimize.Fit(tmpdir, exp, model_set, None, fitness, params,
                       _make_simulation=aju.xml.NeurordSimulation.make,
                       _result_constructor=aju.xml.NeurordResult)
fit.load()
fit.do_fit(iterations, popsize=popsize,sigma=0.3)
mean_dict,std_dict,CV=converge.iterate_fit(fit,test_size,popsize)

########################################### Done with fitting

#to look at centroid [0] or stdev [6] of cloud of good results:
for i,p in enumerate(fit.params.unscale(fit.optimizer.result()[0])):
    print(fit.param_names()[i],'=',p, '+/-', fit.params.unscale(fit.optimizer.result()[6])[i])

#to look at fit history
aju.drawing.plot_history(fit,fit.measurement)

