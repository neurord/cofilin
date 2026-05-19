import os
import numpy as np
import pandas as pd  

# 1. Find files: basal and traces
def search_files(folder, keywords):
    return [f for f in os.listdir(folder) if all(kw in f for kw in keywords)]

def parse_args(commandline,do_exit):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mols',nargs="+",type=str,help='signature/molecule' )
    parser.add_argument('-keys',nargs="+",type=str,help='additional keywords to identify sets of files, same for each molecule' )
    parser.add_argument('-dir', type=str, help = 'give path/to/directory with NeuroRDanal output')
    parser.add_argument('-reg',nargs="+",type=str,help='specify regions to analyze', default=['dend','sa1[0]'] )
    parser.add_argument('-tag_reg',nargs="+",type=str,help='specify spines to analyze as trials', default=[] )
    parser.add_argument('-thresh',nargs="+",type=str,help='specify thresholds for each region analyzed', default=[0.1,0.1] )
    parser.add_argument('-tag_time',type=int,help='specify time of tagging stim', default=None )
    parser.add_argument('-remove',type=str,nargs="+",help='keyword that defines which files to remove',default=[]) #['10u','KO','basal']
    parser.add_argument('-ff',type=str,help='file format', default="csv")
    parser.add_argument('-norm',type=str,help='method for normalization', default='subtract')
    parser.add_argument('-cutoff',type=int,help='filter cutoff frequency, in Hz', default=250)
    parser.add_argument('-col_key',nargs="+",type=str,help='keywords that define separate columns, e.g. massed and spaced')
    parser.add_argument('-color',type=str,help='keyword that defines color scheme, if not 1st word of keys')
    parser.add_argument('-bar',type=str,help='file with bar graph data',default='')
    try:
        args = parser.parse_args(commandline) # maps arguments (commandline) to choices, and checks for validity of choices.
        #if arguments are mapped incorrectly, python wants to exit, but the next line says "don't", instead check whether we are in python (do_exit=False) then don't exit, just give us a warning
    except SystemExit:
        if do_exit:
            raise # raise the exception above (SystemExit) b/c none specified here
        else:
            raise ValueError('invalid ARGS')
    return args

#2 load basal    
def load_basal_means(folder, basal_files,regions=['dend','sa1']):
    basal_data = {reg:{} for reg in regions} 

    #for file in basal_files:
    file=basal_files
    file_path = os.path.join(folder, file)

    with open(file_path, "r") as f:
        header_line = f.readline().strip().replace("\t", " ") #  spacing different and raised error but maybe not (was .T below) check again
        headers = header_line.split() 
        data = np.loadtxt(file_path, delimiter=" ", skiprows=1) 
    
        for reg in regions:
            reg_cols = [i-1 for i, h in enumerate(headers) if reg in h.lower()]                 
            if reg_cols:
                basal_data[reg]['mean'] = np.mean(data[:,reg_cols],axis=1).T 
                basal_data[reg]['std'] = np.std(data[:,reg_cols],axis=1).T 

    basal_data['dt']=data[1,0]        
    return basal_data

#3 load traces 
def load_trace_data(file_path):
    data = np.loadtxt(file_path, delimiter=None, skiprows=1)
    time = data[:, 0]  
    single_traces = data[:, 1:]  
    
    return time, single_traces
    
#4. calculate differnce
def process_mean(header,single_traces,regions=['dend','sa1']):
    trace_means={};trace_sets={}
    for reg in regions:
        reg_cols = [header.index(h)-1 for h in header if reg in h]
        trace_set=single_traces[:,reg_cols]
        trace_mean=np.mean(trace_set,axis=-1)
        trace_means[reg]=trace_mean
        trace_sets[reg]=trace_set
    return trace_means, trace_sets

def remove_files(traces_files,pdir,remove_keys,par_keys=[]):
    for key in remove_keys:
        remove_keywords = par_keys+[key]
        remove_files = search_files(pdir, remove_keywords)
        for rf in remove_files:
            if rf in traces_files:
                traces_files.remove(rf)
    return traces_files

def plot_traces(trace_means,trace_sets,dt,title=''):
        from matplotlib import pyplot as plt
        plt.ion()
        fig,axes=plt.subplots(2,1)
        fig.suptitle(title)
        for ax,reg in enumerate(trace_means.keys()):
            time=np.arange(len(trace_means[reg]))*dt
            for i,trace in enumerate(trace_sets[reg].T):
                axes[ax].plot(time,trace,label=reg+str(i))
            axes[ax].plot(time,trace_means[reg],color='k',label=reg+'_mean')
            axes[ax].set_ylabel(reg)
        axes[ax].set_xlabel('Time (sec)')

def spine_reg(pars):
    bracket=pars.tag_reg[0].find('[')
    spine_name=pars.tag_reg[0][0:bracket] #removes [#] from spine name
    sp_regs=[reg for reg in pars.reg+pars.tag_reg if spine_name in reg]
    dend_reg=[reg for reg in pars.reg if spine_name not in reg][0] #assumes only 1 dend region
    return sp_regs,dend_reg,spine_name

# 7. Save results
def save_results(results, filename, sigmol,trial_count, pars):

    def update_output(par_mol,sigmol,row_data,all_data):
        for tr in row_data.keys():
            row_data[tr]['Trial']=tr
            row_data[tr]['Par']=par_mol.replace('_'+sigmol,'')
            row_data[tr]['sigmol']=sigmol
            all_data.append(row_data[tr])
        return all_data

    filename=filename+sigmol
    if pars.ff == "print":
        for par_mol, regions in results.items():
            print(f"Results for Parameter Molecule: {par_mol}")
            for region, trials in regions.items():
                print(f"  Region: {region}")
                for trnum,row in trials.items():
                    print(f"        {trnum} {row}")
            print("-" * 40)

    elif pars.ff == "txt":
        with open(filename + ".txt", "w") as f:
            for par_mol, regions in results.items():
                f.write(f"Results for Parameter Molecule: {par_mol}\n")
                for region, trials in regions.items():
                    f.write(f"  Region: {region}\n")
                    for trnum,row in trials.items():
                        f.write(f"    {trnum} {trials}\n")
                f.write("-" * 40 + "\n")

    elif pars.ff in ["csv", "xlsx"]:
        all_data = []
        if len(pars.tag_reg):
            sp_regs,dend_reg,spname=spine_reg(pars)
            for par_mol in results.keys():
                row_data={sp+str(trnum):{} for trnum in range(trial_count) for sp in sp_regs} 
                for region in sp_regs:
                    for (trnum,sptrials),dendtrials in  zip(results[par_mol][region].items(),results[par_mol][dend_reg].values()):
                        for (key,val),(dkey,dval) in zip(sptrials.items(),dendtrials.items()):
                            row_data[region+str(trnum)][key+'_'+spname]=val
                            row_data[region+str(trnum)][dkey+'_'+dend_reg]=dval
                all_data=update_output(par_mol,sigmol,row_data,all_data)
        else:
            for par_mol, regions in results.items():
                row_data={trnum:{} for trnum in range(trial_count)} 
                for region, trials in regions.items():
                    if '[' in region:
                        bracket=region.find('[')
                        reg=region[0:bracket]
                    else:
                        reg=region
                    for trnum,trialdata in trials.items():
                        for key,val in trialdata.items():
                            row_data[trnum][key+'_'+reg]=val
                all_data=update_output(par_mol,sigmol,row_data,all_data)

        df = pd.DataFrame(all_data)

        if pars.ff == "csv":
            df.to_csv(filename + ".csv", index=False)
        elif pars.ff == "xlsx":
            with pd.ExcelWriter(filename + ".xlsx") as writer:
                df.to_excel(writer, index=False)

    else:
        print(f"Error: Unknown file format '{pars.ff}'. Please choose from 'print', 'txt', 'csv', or 'xlsx'.")

