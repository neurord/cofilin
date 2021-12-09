#How to use :doc:`ajustador` to fit a NeuroRD model to experimental data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''This demonstration fits a single reaction model (Model_pSynGap) to data.
'''

import ajustador as aju
import numpy as np
from ajustador import drawing,loadconc,nrd_fitness,xml #(line 8)
from ajustador.helpers import converge
import os

#model is the xml file that contains the neuroRD model to simulate and adjust parameters
dirname='./'  #where data and model are stored.  Multiple datafiles allowed
model_set='Model_Cof-Saneyoshi'
exp_name='Saneyoshi_Neuron_2019' #name of data file selected from dirname; each file may contain several molecules
mol=['KalCKpCamCa4','RacGTP'] #which molecule(s) to match in optimization
tmpdir='/tmp/'+dirname+model_set.split('-')[-1]
start_time=10 #time of onset of stimulation, in seconds; should be able to extract from model files; stim time must match data
norm_method='percent'#convert molecule concentration into a percent change from baseline.  Use for comparing to FRET data


# number of iterations, use 1 for testing
# default popsize=8, use 3 for testing
iterations=1
popsize=3
test_size=3#25

os.chdir(dirname)
exp=loadconc.CSV_conc_set(exp_name,stim_time=start_time)

P = xml.XMLParam #xml.XMLParam (use this is line 8 ',xml' is uncomment) else aju.xml.XMLParam 
#list of parameters to change/optimize
params = aju.optimize.ParamSet(P('phos_fwd_rate', 0.00005e-3, min=0.000001e-3, max=0.001e-3, xpath='//Reaction[@id="Kal+CKpCamCa4--KalCKpCamCa4"]/forwardRate'),
                               P('phos_rev_rate', 0.04e-3, min=0.001e-3, max=0.1e-3, xpath='//Reaction[@id="CKpCamCa4+Kal--KalCKpCamCa4"]/reverseRate'),
                               P('phos_kcat_rate', 0.01e-3, min=0.001e-3, max=0.1e-3, xpath='//Reaction[@id="KalCKpCamCa4--pKal+CKpCamCa4]/forwardRate'),
                               P('phos_fwd_rate', 0.0001875e-3, min=0.00001e-3, max=0.01e-3, xpath='//Reaction[@id="RacGDP+pKal--RacGDPpKal"]/forwardRate'),
                               P('phos_rev_rate', 0.15e-3, min=0.01e-3, max=1e-3, xpath='//Reaction[@id="RacGDP+pKal--RacGDPpKal"]/reverseRate'),
                               P('phos_kcat_rate', 0.0375e-3, min=0.001e-3, max=0.1e-3, xpath='//Reaction[@id="RacGDP+pKal--RacGTP+pKal"]/forwardRate'))

                               #P('Kal_conc', 1000, min=1,max=10e3,xpath='//NanoMolarity[@specieID="Kal"]'),
                               #P('Rac_conc', 1000, min=1,max=10e3,xpath='//NanoMolarity[@specieID="RacGDP"]'))


###################### END CUSTOMIZATION #######################################

fitness = nrd_fitness.specie_concentration_fitness(species_list=mol, norm=norm_method)

############ Test fitness function
#sim = aju.xml.NeurordSimulation('/tmp', model=model, params=params)
#cp /tmp/???/model.h5 modelname.split('.')[0]+'.h5'
#sim2=aju.xml.NeurordResult('Model_syngap_ras.h5')
#print(fitness(sim2, exp))
################

fit = aju.optimize.Fit(tmpdir, exp, model_set, None, fitness, params,
                       _make_simulation=xml.NeurordSimulation.make,
                       _result_constructor=xml.NeurordResult)
fit.load()
#fit.do_fit(iterations, popsize=popsize,sigma=0.3)
fit.do_fit(iterations, popsize=popsize, seed=62839)
#mean_dict,std_dict,CV=converge.iterate_fit(fit,test_size,popsize)

########################################### Done with fitting

#to look at centroid [0] or stdev [6] of cloud of good results:
for i,p in enumerate(fit.params.unscale(fit.optimizer.result()[0])):
    print(fit.param_names()[i],'=',p, '+/-', fit.params.unscale(fit.optimizer.result()[6])[i])

#to look at fit history
aju.drawing.plot_history(fit,fit.measurement,Norm='percent')

