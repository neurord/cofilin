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
def total_species (tot_mol,region,files_df,exp_name):
    total_array={to_mol:{reg:np.zeros(len(files_df)) for reg in region} for to_mol in tot_mol.keys()}
    for t_mol, l_mol in tot_mol.items():
        for reg in region:
            for mol in l_mol:
                tcolumn_name=mol+"_"+exp_name+"_"+reg   
                total_array[t_mol][reg]+=files_df[tcolumn_name].values
    return total_array

def ratio_accrosstime(index,files_df,region,denom_mol,num_mol,mov_avg_filt,exp_name):
    #this is used to calculate ratio accross time
    denom_array={reg:np.zeros(len(files_df)) for reg in region}
    num_array={reg:np.zeros(len(files_df)) for reg in region}

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
    return ratio, denom_array, num_array

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
#ratio accross time
ratio_accross,denom_array,num_array=ratio_accrosstime(index,files_df,region,denom_mol,num_mol,mov_avg_filt,exp_name)
#ratio at an interval of time       
tindex_dict={}
for t in time:
    tindex_dict[tuple(t)]=(index(t[0],files_df),index(t[1],files_df))
ratio_interval=measurments(region,tindex_dict,denom_mol,denom_array,num_array)
#total molecules calling
total_molecules=total_species(tot_mol,region,files_df,exp_name)

##############ploting###########

#ratio

for reg,source in ratio_interval.items():
    labl=reg
    plt.bar([str(i) for i in source.keys()], [data for data in source.values()],label=labl)
    plt.legend()
   
###################pairing

for pair in mol_pairs:
    #fig=[]
    fig,axes=plt.subplots(len(region),1,sharex=True)
    fig.suptitle('---'.join(pair))
    for ax,reg in enumerate(region):
        labl=reg          
        if pair[0] and pair[1] in total_molecules:
            X=total_molecules[pair[0]][reg]
            Y=total_molecules[pair[1]][reg]
            axes[ax].plot(X,Y, label=labl, linestyle='--')
        elif pair[0] in total_molecules:
            X=total_molecules[pair[0]][reg]
            Y=files_df[pair[1]+"_"+exp_name+"_"+reg]
            axes[ax].plot(X,Y, label=labl, linestyle='--')
        elif pair[1] in total_molecules:
            X=files_df[pair[1]+"_"+exp_name+"_"+reg]
            Y=total_molecules[pair[0]][reg]
            axes[ax].plot(X,Y, label=labl, linestyle='--')
        else:
            X=files_df[pair[0]+"_"+exp_name+"_"+reg]
            Y=files_df[pair[1]+"_"+exp_name+"_"+reg]
            axes[ax].plot(X,Y, label=labl, linestyle='--')
        
        axes[ax].legend()
        axes[ax].set_ylabel(pair[1])
    axes[ax].set_xlabel(pair[0])
    #plt.show()
        

#ratio accross time
import numpy
times=np.unique(files_df.Time)[~numpy.isnan(np.unique(files_df.Time))]
#Times=times[~numpy.isnan(times)]#somehow, shape is change so used numpy
fig,axes=plt.subplots(len(reg),1,sharex=True)
#fig.suptitle('---'.join(str(list(num_mol),'/',list(denom_mol))))
for ax,reg in enumerate(ratio_accross.keys()):
    labl=reg
    axes[ax].plot(times,ratio_accross[reg],label=labl)  
    axes[ax].legend()
    axes[ax].set_ylabel('ratio')
axes[ax].set_xlabel('Time')
