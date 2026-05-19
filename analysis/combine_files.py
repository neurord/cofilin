import numpy as np
from normalize import load_data
names=['Model_Cof_10um3spines_basal_CK_PKA_PAK_sig_trials.txt','Model_Cof_10um3spines_basal_kinase_sig_trials.txt']
fnames=[['Model_Cof-ctrl-4trbasal-CK_PKA_PAK-sig-trials.txt', 'Model_Cof-ctrl-4trbasal2-CK_PKA_PAK-sig-trials.txt'],
        ['Model_Cof-ctrl-4trbasal-CK_PKA-sig-trials.txt', 'Model_Cof-ctrl-4trbasal2-CK_PKA-sig-trials.txt'],
        ['Model_Cof-ctrl-4trbasal-kinase-sig-trials.txt', 'Model_Cof-ctrl-4trbasal2-kinase-sig-trials.txt'],
        ['Model_Cof-ctrl-4trbasal-cof_act-sig-trials.txt', 'Model_Cof-ctrl-4trbasal2-cof_act-sig-trials.txt']]
fnames=[['Model_Cof-ctrl-4trspaced-KalCKCamCa4-avg.txt','Model_Cof-ctrl-4trspaced-KalCKpCamCa4-avg.txt'],
         ['Model_Cof-KOCK2-4trspaced-KalCKCamCa4-avg.txt','Model_Cof-KOCK2-4trspaced-KalCKpCamCa4-avg.txt'], 
        ['Model_Cof-PDE4enh-4trspaced-KalCKCamCa4-avg.txt','Model_Cof-PDE4enh-4trspaced-KalCKpCamCa4-avg.txt'],
        ['Model_Cof-PDE4red-4trspaced-KalCKCamCa4-avg.txt','Model_Cof-PDE4red-4trspaced-KalCKpCamCa4-avg.txt'],       
        ['Model_Cof-KOPKA-4trspaced-KalCKCamCa4-avg.txt','Model_Cof-KOPKA-4trspaced-KalCKpCamCa4-avg.txt']]
fnames=[['Model_Cof-constrBosch-totCof-trials.txt','Model_Cof-constrBosch2-totCof-trials.txt']]
fmolname=['KalCKtot']*len(fnames) #only used for sum
desired_length=18001 #only used for interp
dirname='resultsCKhalf2/'
process_type='concat' ##choices are: 'sum' , 'concat', 'interp' 

def concat_data(fnames,dirname):
    if len(dirname):
        fnames=[dirname+fn for fn in fnames]
    outfname=fnames[0].split('trials')[0]+'alltrials.txt'
    data,headers,_=load_data(fnames[0])
    for fnm in fnames[1:]:
        data2,header2,_=load_data(fnm)
        data=np.column_stack([data,data2[:,1:]]) #combine files into one
        #find maximum trial number
        trial_nums=[int(tr.split('_tr')[-1]) for tr in headers[1:]]
        num_trials=np.max(trial_nums)+1
        #renumber trial num in header in subsequent files
        new_head2=[tr.split('_tr')[0]+'_tr'+str(int(tr.split('_tr')[-1])+num_trials) for tr in header2[1:]]
        headers=headers+new_head2 #combine headers into one
    np.savetxt(outfname,data,header=' '.join(headers))
    return headers, np.shape(data)

def sum_data(fnames,dirname,molname):
    if len(dirname):
        fnames=[dirname+fn for fn in fnames]
    data,headers,_=load_data(fnames[0])
    orig_mol=fnames[0].split('-')[-2]
    new_head=headers[0:1]+[h.replace(h.split('_')[0],molname) for h in headers[1:]]
    for fnm in fnames[1:]:
        data2,header2,_=load_data(fnm)
        data=data+data2
        data[:,0]=data2[:,0] #fix the time column
    outfname=fnames[0].replace(orig_mol,molname)
    np.savetxt(outfname,data,header=' '.join(new_head))
    return new_head, np.shape(data)

def interpolate(fname,desired_length):
    data,headers,_=load_data(fname)
    time=data[:,0]
    dt=time[1]-time[0]
    time_factor=(desired_length-1)/(len(time)-1)
    desired_time=np.arange(desired_length)*dt/time_factor #
    newdata=np.zeros((desired_length,np.shape(data)[1])) #initialize array
    newdata[:,0]=desired_time #put new time vector into array
    outfname=fname.split('.')[0]+'interp.txt'
    for i in range(1,np.shape(data)[1]-1):
        newdata[:,i]=np.interp(desired_time, time, data[:,i]) #interpolate all columns into array
    np.savetxt(outfname,data,header=' '.join(headers))

if process_type == 'concat':
    for fset in fnames:
        header,shape=concat_data(fset,dirname)
        print('header',len(header),'data shape',shape)
elif process_type =='sum':
    for fset,mn in zip(fnames,fmolname):
        header,shape=sum_data(fset,dirname,mn)
        print('header',len(header),'data shape',shape)
elif process_type=='interp':
    if len(dirname):
        fnames=[dirname+fn for fn in fnames]
    for fn in fnames:
        interpolate(fn,desired_length)


