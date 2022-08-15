#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''trying to fit cof to bosh data '''


import ajustador as aju
import numpy as np
from ajustador import drawing,loadconc,nrd_fitness
from ajustador.helpers import converge,save_params
import os

dirname='cof_opt_basal300'
#name of model xml file for optimization
model_set='Model_Cof_fitbasal_aju133-811.xml'
#name of experimental data, a simulation file in this case
exp_name='Bosch_Hedrick_cof-basal300'
#molecule to compare between 'experiments' and simulations
mol={'RacPAK':['RacPAK','RacGTP'],'Cofactin':['Cof', 'Cofactin']}#mol={'RacGTP': ['RacGTP'],'Cof':['Cof','Cofactin']}
#directory to store output during optimization
tmpdir='/tmp/'+dirname+'ajustim'
start_stim=90 # time stim start sec 
#norm_method ='percent'


# number of iterations, use 1 for testing
iterations=100
# default popsize=8, use 3 for testing
popsize=8
test_size=25
rootdir='./' ### doesn't work if using at
if not dirname in os.listdir(rootdir):
    os.mkdir(rootdir+dirname)
#use #2 exp since loading exp 
#exp = aju.xml.NeurordResult(exp_set)
#this command indicates that experimental data are concentration in csv formatted files
os.chdir(dirname)
exp=loadconc.CSV_conc_set(exp_name,
                          stim_time=start_stim)
#print('***********************************',exp.data[0].waves['Cof'].wave)
#specify parameters to vary, either from ReactionScheme or InitialConditions
P = aju.xml.XMLParam
#Double check. #2
params = aju.optimize.ParamSet(P('Racact_fwd_rate',1.3e-6, min=2e-8, max=2e-4, xpath='//Reaction[@id="RacGDP+Kal--pKalRacGDP"]/forwardRate'),
                               P('Racact_bckd_rate',4.7e-5, fixed='Racact_kcat_rate',constant=4, xpath='//Reaction[@id="RacGDP+Kal--pKalRacGDP"]/reverseRate'),
                               P('Racact_kcat_rate',1.2e-5, min=1.5e-7, max=1.5e-3, xpath='//Reaction[@id="pKalRacGDP--pKal+RacGTP"]/forwardRate'),
                               P('PAKact_fwd_rate',3.1e-5, min=3.1e-7, max=3.1e-3, xpath='//Reaction[@id="RacGTP+PAK--RacGTPPAK"]/forwardRate'),
                               P('PAKact_bckd_rate',0.004, min=0.004e-2, max=0.004e2, xpath='//Reaction[@id="RacGTP+PAK--RacGTPPAK"]/reverseRate'),
                               P('LIMKact_fwd_rate',0.0012, min=0.0012e-2, max=0.0012e2, xpath='//Reaction[@id="RacPAK+LIMK--LIMKRacPAK"]/forwardRate'),
                               P('LIMKact_bckd_rate',1.02, fixed='LIMKact_kcat_rate',constant=4, xpath='//Reaction[@id="RacPAK+LIMK--LIMKRacPAK"]/reverseRate'),
                               P('LIMKact_kcat_rate',0.25, min=0.3e-2, max=0.3e2, xpath='//Reaction[@id="LIMKRacPAK--RacPAK+pLIMK"]/forwardRate'),
                               P('SSHact_fwd_rate',3.3e-5, min=3.3e-7, max=3.3e-3, xpath='//Reaction[@id="CaNCamCa4+pSSH--CaNCamCa4pSSH"]/forwardRate'),
                               P('SSHact_bckd_rate',0.003,fixed='SSHact_kcat_rate',constant=4 , xpath='//Reaction[@id="CaNCamCa4+pSSH--CaNCamCa4pSSH"]/reverseRate'),
                               P('SSHact_kcat_rate',0.0007, min=0.0007e-2, max=0.0007e2, xpath='//Reaction[@id="CaNCamCa4pSSH--SSH+CaNCamCa4"]/forwardRate'),
                               P('Cofact_fwd_rate',2.29e-5, min=2.29e-7, max=2.29e-3, xpath='//Reaction[@id="pCof+SSH--SSHpCof"]/forwardRate'),
                               P('Cofact_bckd_rate',0.56, fixed='Cofact_kcat_rate',constant=4, xpath='//Reaction[@id="pCof+SSH--SSHpCof"]/reverseRate'),
                               P('Cofact_kcat_rate',0.14, min=0.14e-2, max=0.14e2, xpath='//Reaction[@id="SSHpCof--Cof+SSH"]/forwardRate'),
                               P('actinact_fwd_rate',4.32e-6, min=4.32e-8, max=4.32e-4, xpath='//Reaction[@id="actin+Cof--Cofactin"]/forwardRate'),
                               P('actinact_bckd_rate',0.0098, min=0.01e-2, max=0.01e2, xpath='//Reaction[@id="actin+Cof--Cofactin"]/reverseRate'),
                               P('LIMKinact_fwd_rate',0.001, min=0.001e-2, max=0.001e2, xpath='//Reaction[@id="pLIMK+SSH--SSHpLIMK"]/forwardRate'),
                               P('LIMKinact_bckd_rate',3.31, fixed='LIMKinact_kcat_rate',constant=4, xpath='//Reaction[@id="pLIMK+SSH--SSHpLIMK"]/reverseRate'),
                               P('LIMKinact_kcat_rate',0.83, min=0.83e-2, max=0.83e2, xpath='//Reaction[@id="SSHpLIMK--pLIMK+SSH"]/forwardRate'),
                               P('SSHinact_fwd_rate',2.13e-5, min=2.13e-7, max=2.13e-3, xpath='//Reaction[@id="RacPAK+SSH--SSHRacPAK"]/forwardRate'),
                               P('SSHinact_bckd_rate',0.18, fixed='SSHinact_kcat_rate',constant=4, xpath='//Reaction[@id="RacPAK+SSH--SSHRacPAK"]/reverseRate'),
                               P('SSHinact_kcat_rate',0.46, min=0.46e-2, max=0.46e2, xpath='//Reaction[@id="SSHRacPAK--pSSH+RacPAK"]/forwardRate'),
                               P('Cofinact_fwd_rate',0.0033, min=0.0033e-2, max=0.0033e2, xpath='//Reaction[@id="Cof+pLIMK--pLIMKCof"]/forwardRate'),
                               P('Cofinact_bckd_rate',0.4, fixed='Cofinact_kcat_rate',constant=4, xpath='//Reaction[@id="Cof+pLIMK--pLIMKCof"]/reverseRate'),
                               P('Cofinact_kcat_rate',0.1, min=0.1e-2, max=0.1e2, xpath='//Reaction[@id="pLIMKCof--pCof+pLIMK"]/forwardRate'))

#this command indicates that experiments are from a previous simulation
###################### END CUSTOMIZATION #######################################

fitness = nrd_fitness.specie_concentration_fitness(species_list=mol,start=start_stim)

fit = aju.optimize.Fit(tmpdir, exp, model_set, None, fitness, params,
                       _make_simulation=aju.xml.NeurordSimulation.make,
                       _result_constructor=aju.xml.NeurordResult)
fit.load()
fit.do_fit(iterations, sigma=0.3,popsize=popsize)
mean_dict,std_dict,CV=converge.iterate_fit(fit,test_size,popsize)
########################################### Done with fitting

#to look at centroid [0] or stdev [6] of cloud of good results:
if callable(fit.optimizer.result):
    result=fit.optimizer.result()
else:
    result=fit.optimizer.result
for i,p in enumerate(fit.params.unscale(result[0])):
        print(fit.param_names()[i],'=',p, '+/-', fit.params.unscale(result[6])[i])


#to save
save_params.save_params(fit,0,1)

#to look at fit history
aju.drawing.plot_history(fit,fit.measurement,mol_dict=mol)

'''
fit[830]                  
NeurordSimulation(<TemporaryDirectory '/tmp/cof_opt/tmprom761ve'>

*************** optimization converged at 0 with m= 0.38459888633036704
*************** optimization converged at 200 with m= 0.3718750411155398
*************** optimization converged at 400 with m= 0.3828367857551935
**************  optimization NOT converged 600 m= 0.33132277813542976
*************** optimization converged at 800 with m= 0.31682237301114896
end of iterate_fit.py cof_opt len of fitness 1000 last_j 5 len(mean_dict) 5
Racact_fwd_rate = 1.2106438509014752e-07 +/- 3.205943287317544e-09
Racact_kcat_rate = 3.191684174483173e-05 +/- 6.733659228341633e-07
PAKact_fwd_rate = 1.2855342315141675e-05 +/- 1.1053498387882872e-07
PAKact_bckd_rate = 0.0018297780934014524 +/- 1.6936387897028285e-05
LIMKact_fwd_rate = 0.0031882398506731225 +/- 5.56061754660724e-05
LIMKact_kcat_rate = 0.058777648045564526 +/- 0.000996389977509354
SSHact_fwd_rate = 2.868778905737035e-06 +/- 6.023113961744283e-08
SSHact_kcat_rate = 9.979647942591331e-05 +/- 1.381976693897793e-06
Cofact_fwd_rate = 4.972222932554047e-06 +/- 1.2260185538710978e-07
Cofact_kcat_rate = 0.3735582010534191 +/- 0.003926755139785789
actinact_fwd_rate = 1.5106484906625724e-08 +/- 5.668342437056704e-11
actinact_bckd_rate = 0.0009392079674340111 +/- 1.1022216210138052e-05
LIMKinact_fwd_rate = 0.0001352746368047536 +/- 1.8159499467142406e-06
LIMKinact_kcat_rate = 0.024214401564152385 +/- 0.00032066194270299436
SSHinact_fwd_rate = 0.00011791766049226193 +/- 1.3860033413869288e-06
SSHinact_kcat_rate = 0.0417416425954855 +/- 0.00024913021721035693
Cofinact_fwd_rate = 0.0010370753216020405 +/- 1.4881874977545987e-05
Cofinact_kcat_rate = 0.05695041546323296 +/- 0.00019545764587265937
'''
