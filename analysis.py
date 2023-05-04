import glob
import os 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.ion()
####################################################
'''
try:
    args = ARGS.split()
    print("ARGS =", ARGS, "commandline=", args)
    do_exit = False
except NameError: #NameError refers to an undefined variable (in this case ARGS)
    args = sys.argv[1:]
    import os
    mydir=os.getcwd()
    sys.path.append(mydir)
    print("commandline =", args)
    do_exit = True

except Exception:
    pass
'''
##########################################################

def get_data(files_folder,globpattern):
    files=[]
    # Create a dataframe list by using a list comprehension
    files=[pd.read_csv(fil, sep=" ", header=[0]) for fil in glob.glob(os.path.join(files_folder,globpattern))]
    # Concatenate the list of DataFrames into one
    files_df=pd.concat(files,axis=1,ignore_index=False)
    #get main columns 
    main_col=[C for C in files_df.columns if not C.endswith('std')]
    return main_col, files_df

def index(t,files_df):
    return np.min(np.where(np.unique(files_df.Time)>t))

def measurments(region,tindex_dict,denom_mol,denom_array,num_array):
#this is used for calculating single value at certain time point such as pre-stim, post_stim ...
    nmeas_dict={reg:{} for reg in region}
    dmeas_dict={reg:{} for reg in region}
    for reg in region:
        for temps,ind in tindex_dict.items():
            dmeas_dict[reg][temps]=1 if not denom_mol else denom_array[reg][ind[0]:ind[1]].mean()
            nmeas_dict[reg][temps]=num_array[reg][ind[0]:ind[1]].mean()
        if not denom_mol:
            ratio_meas=nmeas_dict    
        else:
            ratio_meas={reg:{k:nmeas_dict[reg][k]/dmeas_dict[reg][k] for k in nmeas_dict[reg].keys()} for reg in region}
    return ratio_meas

#create total molecues
#total_array={to_mol:{reg:np.zeros(len(files_df)) for reg in region} for to_mol in tot_mol.keys()}
def total_species (tot_mol,region,files_df,exp_name):
    for t_mol, l_mol in tot_mol.items():
        for reg in region:
            for mol in l_mol:
                tcolumn_name=mol+"_"+exp_name+"_"+reg   
                total_array[t_mol][reg]+=files_df[tcolumn_name].values
    return total_array

def ratio_accrosstime(index,files_df,region,denom_mol,num_mol,mov_avg_filt,exp_name):
    #this is used to calculate ratio accross time
    for reg in region:
        if not denom_mol:
            denom_array[reg]=1
        else:
            for d_mol in denom_mol:
                dcolumn_name=d_mol+"_"+exp_name+"_"+reg
                denom_array[reg]+=files_df[dcolumn_name].values            
        for n_mol in num_mol:
            ncolumn_name=n_mol+"_"+exp_name+"_"+reg
            num_array[reg]+=files_df[ncolumn_name].values
    if not denom_mol:
        ratio=num_array    
    else:
        with np.errstate(divide='ignore'):##might raised plotting error
            ratio={reg:num_array[reg]/denom_array[reg] for reg in region}   
    if filt_length>1:   
        for reg in ratio.keys():
                ratio[reg]=np.convolve(mov_avg_filt,ratio[reg],'same')
    return ratio

###variable###
######change everytime#####
denom_mol=['Cofactin','Cof']
num_mol=['pCof']
time=[[0,200],[200,202],[202,399]]#in sec
tot_mol={'actCof':['Cof','Cofactin'],'inacCof':['pCof','Cof']}
mol_pairs=[['actCof','inacCof'],['pCof','Cofactin']]
##############args#########
exp_name="1"
globpattern="Model_Cof*"+"_avg.txt"
fname=glob.glob(globpattern)
#print(fname)
files_folder='./'
filt_length=9
mov_avg_filt=np.ones(filt_length)/filt_length
plot=0

  
#get region
main_col,files_df=get_data(files_folder,globpattern)
region=np.unique([r.split("_")[-1] for r in main_col if r!='Time' and not r.endswith('All')])#fix for all
#create arrays for denominators or numerators mol
denom_array={reg:np.zeros(len(files_df)) for reg in region}
num_array={reg:np.zeros(len(files_df)) for reg in region}

#ratio accross time
ratio_accross=ratio_accrosstime(index,files_df,region,denom_mol,num_mol,mov_avg_filt,exp_name)
#ratio at an interval of time       
tindex_dict={}
for t in time:
    tindex_dict[tuple(t)]=(index(t[0],files_df),index(t[1],files_df))
ratio_interval=measurments(region,tindex_dict,denom_mol,denom_array,num_array)
#total molecules calling
total_array={to_mol:{reg:np.zeros(len(files_df)) for reg in region} for to_mol in tot_mol.keys()}
total_molecules=total_species(tot_mol,region,files_df,exp_name)

for reg,source in ratio_interval.items():
    labl=reg
    for inter, data in source.items():
        plt.bar([str(i) for i in inter],data,label=labl)
    plt.legend()
    plt.show()

###################pairing
'''
#get molecules list 
mol_list=[]
pair_ext={reg:[] for reg in region}
for m in files_df.columns:
    mol_list.append(m.split('_')[0])
    mollist=np.unique(mol_list)
for reg in region:
    for pair in mol_pairs:
        pair_ext[reg][pair]=[]
        for mol in pair:
          pair_fullname=mol+"_"+exp_name+"_"+reg  
          pair_ext[pair][reg].append(pair_fullname)
'''

for pair in mol_pairs:
    fig=[]
    for reg in region:
        labl=reg
        plt.figure()
        plt.title('---'.join(pair))
        if pair[0] and pair[1] in total_molecules:
            X=list(total_molecules[pair[0]])
            Y=list(total_molecules[pair[1]])
        elif pair[0] in total_molecules:
            X=list(total_molecules[pair[0]])
            Y=files_df[pair[1]+"_"+exp_name+"_"+reg]
        elif pair[1] in total_molecules:
            X=files_df[pair[1]+"_"+exp_name+"_"+reg]
            Y=list(total_molecules[pair[0]])
        else:
            X=files_df[pair[0]+"_"+exp_name+"_"+reg]
            Y=files_df[pair[1]+"_"+exp_name+"_"+reg]
        f,a=plt.subplots(len(pair),len(reg))
        plt.plot(X,Y, label=labl, linestyle='--')
        fig.append(f)
        plt.xlabel(pair[1])
        plt.ylabel(pair[0])
        plt.legend()
        plt.show()
        

