import numpy as np
import os
fnames=[['Model_Cof-PDE4enh-4trbasal-pLIMKall-trials.txt', 'Model_Cof-PDE4enh-4trbasal-LIMKall-trials.txt','Model_Cof-ctrl-4trbasal-pLIMKall-trials.txt', 'Model_Cof-ctrl-4trbasal-LIMKall-trials.txt'],
['Model_Cof-PDE4enh-4trbasal-pCoftot-trials.txt', 'Model_Cof-PDE4enh-4trbasal-actCof-trials.txt','Model_Cof-ctrl-4trbasal-pCoftot-trials.txt', 'Model_Cof-ctrl-4trbasal-actCof-trials.txt']]
#fnames=[['Model_Cof-constrBosch-totCof-alltrials.txt']]#'Model_Cof-Hedrick-RacPAK-trials.txt','Model_Cof-constrHedrick-RacPAK-avg.txt','Model_Cof-constrBosch-totCof-avg.txt','Model_Cof-Bosch-totCof-trials.txt']],['Model_Cof-constrHedrick-RacPAKtot-avg.txt']
dirname='resultsCKhalf2/'
onset_time=300
regions=['dend','sa1[0]'] #'All',
save=True
plot='norm'
mean_from_trials=True
trial_word='_tr' #'trial' for previous NeuroRDanal outputs

def init(fname,plot):
    if fname.split('.')[0].endswith('avg'):
        reg_cols={'mean':[],'std':[]}
    elif fname.split('.')[0].endswith('trials'):    
        reg_cols={trial_word:[]}
        #if plot:
        #    plot=True
    return reg_cols,plot

def plot_data(data,time,regions,label):
    from matplotlib import pyplot as plt
    plt.ion()
    plt.figure()
    for reg in regions:
        for coltype in data[reg].keys():
            plt.plot(time,data[reg][coltype],label=reg+coltype)
    plt.legend()
    plt.xlabel('Time')
    plt.suptitle(label)
    #plt.show()

def save_data(fname,time,regions,data,colname):    
    outfname=fname.split('.')[0]+'norm.txt'
    output=time
    header='time'
    for reg in regions:
        for tp in colname[reg].keys():
            header=header+'   '+' '.join([cn+'_norm' for cn in colname[reg][tp]])
            output=np.column_stack([output,data[reg][tp]])
    np.savetxt(outfname,output,header=header)

def load_data(fname):
    with open(fname, "r") as f:
        header_line = f.readline().strip().replace("\t", " ")
        headers=header_line.split()[1:]
    data=np.loadtxt(fname,skiprows=1) 
    time=data[:,0]
    return data,headers,time

def process_data(data,headers,regions,reg_cols):   
    reg_data={reg:{} for reg in regions}
    norm_data={reg:{} for reg in regions}
    colnames={reg:{} for reg in regions}
    basal={}
    for reg in regions:
        print('extracting columns for reg=',reg)
        for coltype in reg_cols.keys(): 
            if coltype=='mean':
                reg_cols[coltype] = [i for i, h in enumerate(headers) if reg in h and 'std' not in h.lower()]
            else:  
                reg_cols[coltype]= [i for i, h in enumerate(headers) if reg in h and coltype in h.lower()] 
            if reg=='dend' and coltype !=trial_word:
                reg_cols[coltype]=reg_cols[coltype][0:1] #don't use dendsub/dendcyt
            if len(reg_cols[coltype]):
                reg_data[reg][coltype] = data[:,reg_cols[coltype]]
                colnames[reg][coltype]=[headers[i] for i in reg_cols[coltype]] 
                print('coltype=',coltype,',cols=',reg_cols[coltype],',colnames=',colnames[reg])
        if 'mean' in reg_data[reg]:
            basal[reg]=np.mean(reg_data[reg]['mean'][0:onset_point,0])
            for coltype in reg_cols.keys():
                norm_data[reg][coltype]=reg_data[reg][coltype][:,0]/basal[reg] #0 means use 1st column - which is whole dend
        elif trial_word in reg_data[reg]:
            reg_data[reg]['mean']=np.mean(reg_data[reg][trial_word],axis=1).T 
            norm_data[reg][coltype]=reg_data[reg][coltype]/np.mean(reg_data[reg]['mean'][0:onset_point])
            if mean_from_trials:
                norm_data[reg]['mean']=np.mean(norm_data[reg][trial_word],axis=1).T 
                norm_data[reg]['std']=np.std(norm_data[reg][trial_word],axis=1).T 
                colnames[reg]['mean']=[colnames[reg][trial_word][0].split(trial_word)[0]+'mean']
                colnames[reg]['std']=[colnames[reg][trial_word][0].split(trial_word)[0]+'std']
    return reg_data,norm_data,colnames

#################### Main ###################################
if __name__ == '__main__':
    for fset in fnames:
        basal_mean={reg:{} for reg in regions}
        for fname in fset:
            reg_cols,plot=init(fname,plot)
            if len(dirname):
                fname=dirname+fname
            data,headers,time,=load_data(fname)
            dt=time[1]
            onset_point=int(onset_time/dt)
            reg_data,norm_data,colnames=process_data(data,headers,regions,reg_cols)
            basal_word=[x for x in fname.split('-') if 'basal' in x]
            if len(basal_word):
                parts=os.path.basename(fname).split('-'+basal_word[0]+'-')
                if parts[-1].startswith('1-'):
                    mol_loc=1
                else:
                    mol_loc=0
                fkey=parts[-1].split('-')[mol_loc]+'-'+parts[0].split('-')[-1]
                for reg in regions:
                    if trial_word in reg_data[reg].keys():
                        basal_mean[reg][fkey]=np.mean(reg_data[reg][trial_word],axis=0)
                    else:
                        basal_mean[reg][fkey]=np.mean(reg_data[reg]['mean'])
            if save:#FIXME: extract columnname
                save_data(fname,time,regions,norm_data,colnames)

            if plot=='norm':
                plot_data(norm_data,time,regions,label=fname)
            elif plot:
                plot_data(reg_data,time,regions,label=fname)

        for reg in regions:
            print('region=',reg)
            for fkey in basal_mean[reg].keys():
                print(fkey,np.round(basal_mean[reg][fkey],2)) #print these values to calculate ratios
        spvol=.06493
        dendvol=1.056
        if 'pCoftot-PDE4enh' in basal_mean['dend'].keys():
            enh_ratio=(dendvol*basal_mean['dend']['pCoftot-PDE4enh']+spvol*basal_mean['sa1[0]']['pCoftot-PDE4enh'])/(dendvol*basal_mean['dend']['actCof-PDE4enh']+spvol*basal_mean['sa1[0]']['actCof-PDE4enh'])
            ctrl_ratio=(dendvol*basal_mean['dend']['pCoftot-ctrl']+spvol*basal_mean['sa1[0]']['pCoftot-ctrl'])/(dendvol*basal_mean['dend']['actCof-ctrl']+spvol*basal_mean['sa1[0]']['actCof-ctrl'])
        elif 'pLIMKall-PDE4enh' in basal_mean['dend'].keys():
            enh_ratio=(dendvol*basal_mean['dend']['pLIMKall-PDE4enh']+spvol*basal_mean['sa1[0]']['pLIMKall-PDE4enh'])/(dendvol*basal_mean['dend']['LIMKall-PDE4enh']+spvol*basal_mean['sa1[0]']['LIMKall-PDE4enh'])
            ctrl_ratio=(dendvol*basal_mean['dend']['pLIMKall-ctrl']+spvol*basal_mean['sa1[0]']['pLIMKall-ctrl'])/(dendvol*basal_mean['dend']['LIMKall-ctrl']+spvol*basal_mean['sa1[0]']['LIMKall-ctrl'])
        else:
            enh_ratio=ctrl_ratio=[]
        if len(ctrl_ratio):
            print(fset)
            print('enh_ratio=',np.round(enh_ratio,3),'ctrl_ratio=',np.round(ctrl_ratio,3), 'norm ctrl std=',round(np.std(ctrl_ratio)/np.mean(ctrl_ratio),3))
            if len(ctrl_ratio)==len(enh_ratio): 
                print('ratio of ratios=',np.round(enh_ratio/ctrl_ratio,3),'mean+/-std=',round(np.mean(enh_ratio/ctrl_ratio),3),round(np.std(enh_ratio/ctrl_ratio),3))
            else:
                max_len=min(len(ctrl_ratio),len(enh_ratio))
                print('ratio of ratios=',np.round(enh_ratio[0:max_len]/ctrl_ratio[0:max_len],3),'mean+/-std=',round(np.mean(enh_ratio[0:max_len]/ctrl_ratio[0:max_len]),3),round(np.std(enh_ratio[0:max_len]/ctrl_ratio[0:max_len]),3))
               
''' 
results2025oct
fnames=['Model_Cof_enh_basal_pLIMKall_trials.txt', 'Model_Cof_enh_basal_LIMKall_trials.txt']
dend=1331, sa1=1181;            dend=664,sa1=829; dend ratio: 2.00
fnames=['Model_Cof-basal-pLIMKall-trials.txt', 'Model_Cof-basal-LIMKall-trials.txt']
dend=1406, sa1=1200;            dend=592,sa1=802; dend ratio: 2.375
ratio of ratios =2.375/2.00= 0.84 - similar to Nadia, goal is 0.75

fnames=['PDE4/Model_Cof_enh_basal_pCoftot_trials.txt', 'PDE4/Model_Cof_enh_basal_actCof_trials.txt']
dend=1744, sa1=1469;            dend=208,sa1= 463; dend ratio: 8.38
fnames=['ctrl/Model_Cof-basal-pCoftot-trials.txt', 'ctrl/Model_Cof__basal_actCof_trials.txt']
dend=1735, sa1=1419;            dend=207,sa1=548; dend ratio: 8.38
ratio of ratios =1 - not at all like experiments

restuls2025dec
region= All
pCoftot-PDE4enh 991.39
actCof-PDE4enh 923.0
PDE4enh:ratio of pCof to actCof = 991/923=1.074
pCoftot-ctrl 1082.42
actCof-ctrl 824.75
CTRL: ratio of pCof to actCof =  1082/825 = 1.312
ratio of ratios=1.074/1.312=0.819 - close to experiments!
Trials (dend+sa1 weighted average):
enh_ratio= [1.319 0.825 1.265 1.044 0.999] ctrl_ratio= [1.442 1.686 0.914 1.382 1.281] norm ctrl std= 0.188, se=.084
ratio of ratios= [0.915 0.489 1.383 0.755 0.78 ] mean+/-std= 0.864 0.294, se=.131

region= All
pLIMKall-PDE4enh 746.22
LIMKall-PDE4enh 1248.92
PDE4enh:ratio of pLIMK:LIMK = 746.22/1248.92= 0.598
pLIMKall-ctrl 848.41
LIMKall-ctrl 1154.15
CTRL: ratio of pLIMK:LIMK = 848.41/1154.15= 0.735 
ratio of ratios: 0.598/0.735 = 0.814  - close to experiments!
Trials (dend+sa1 weighted average):
enh_ratio= [0.66  0.525 0.654 0.559 0.597] ctrl_ratio= [0.764 0.924 0.541 0.762 0.73 ] norm ctrl std= 0.164, se=0.073
ratio of ratios= [0.864 0.569 1.211 0.733 0.818] mean+/-std= 0.839 0.211, se=0.094

RESULTSI1PKA
region=ALL
['Model_Cof-PDE4enh-4trbasal-1-pLIMKall-trials.txt', 'Model_Cof-PDE4enh-4trbasal-1-LIMKall-trials.txt', 'Model_Cof-ctrl-4trbasal-1-pLIMKall-trials.txt', 'Model_Cof-ctrl-4trbasal-1-LIMKall-trials.txt']
pLIMK/LIMK
enh_ratio= [0.696 0.775 0.706 0.652 0.617] ctrl_ratio= [0.969 1.328 0.858 1.528 1.134] norm ctrl std= 0.208, se=.093
ratio of ratios= [0.718 0.583 0.822 0.427 0.544] mean+/-std= 0.619 0.138, se=.062

['Model_Cof-PDE4enh-4trbasal-1-pCoftot-trials.txt', 'Model_Cof-enh-basal-actCof-trials.txt', 'Model_Cof-ctrl-4trbasal-1-pCoftot-trials.txt', 'Model_Cof-ctrl-4trbasal-actCof-trials.txt']
enh_ratio= [1.198 1.459 1.154 1.03  1.062] ctrl_ratio= [1.682 2.508 1.42  3.034 2.156] norm ctrl std= 0.267, se=0.119
ratio of ratios= [0.712 0.582 0.812 0.339 0.493] mean+/-std= 0.588 0.165, se=.073

resultsCKhalf2
region=ALL
enh_ratio= [0.828 0.792 0.743 0.778 0.676] ctrl_ratio= [1.36  1.224 1.142 1.272 1.08  1.15  1.26  1.135 1.134 1.233] norm ctrl std= 0.067
ratio of ratios= [0.609 0.647 0.651 0.611 0.625] mean+/-std= 0.629 0.018

['Model_Cof-PDE4enh-4trbasal-pCoftot-trials.txt', 'Model_Cof-PDE4enh-4trbasal-actCof-trials.txt', 'Model_Cof-ctrl-4trbasal-pCoftot-trials.txt', 'Model_Cof-ctrl-4trbasal-actCof-trials.txt']
enh_ratio= [1.233 1.136 1.066 1.143 0.939] ctrl_ratio= [2.506 2.015 1.807 1.938 1.641 1.876 1.969 1.821 1.765 2.197] norm ctrl std= 0.12
ratio of ratios= [0.492 0.564 0.59  0.59  0.572] mean+/-std= 0.562 0.036
'''