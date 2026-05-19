 #exec(open('/local/vol00/Users/nminingouzobon/cofilin/txt/crtl/dataset_analysis.py').read())
import os
import sys
import numpy as np
import pandas as pd  
from matplotlib import pyplot as plt
import DifferenceCalculator as dc
import utils

#6 process files
def process_files(folder,traces_files, basal_data, onset_times,baseline_times,mol, diff_calc,regions=['dend','sa1'],plot_traces=False):
    results = {}
    
    for file,onset_time,base_time in zip(traces_files, onset_times, baseline_times):
        print('onset time, in process files',onset_time)
        #reinitialize critical points for each file
        diff_calc.rise_point_idx={reg:np.nan for reg in regions}
        diff_calc.drop_point_idx={reg:np.nan for reg in regions}
        diff_calc.end_point_idx={reg:np.nan for reg in regions}
        print('analyzing', file)
        par = file.split(mol)[0].split('Model_Cof')[-1]#this is dangerous # change this when file naming changes
        par_mol = f"{par}_{mol}" #par + "_" + mol
        time, single_traces = utils.load_trace_data(os.path.join(folder, file))
        with open(os.path.join(folder, file), "r") as f:
            header_line = f.readline().strip().split()
        header = [label.lower() for label in header_line[1:]]#header_line[1:]

        baseline_idx = np.min(np.where(time >= base_time)) 
        #smallest is index of stim onset
        #determine thresholds from mean traces.  Use those thresholds all trials
        trace_means,trace_sets=utils.process_mean(header,single_traces,regions=regions)
        if plot_traces:
            utils.plot_traces(trace_means,trace_sets,time[1],title=par) #optionally plot them
        for reg in regions:
            stim_onset_idx = np.min(np.where(time >= onset_time[reg])) 
            diff_calc.find_points(time,stim_onset_idx,baseline_idx, trace_means[reg],basal_data,reg,ylbl=mol+par) #find critical points from mean traces
        file_results = {}
        trial_count = {reg:0 for reg in regions} #{"dend": 0, "sa1": 0}

        # Process each trial
        for region,traces in trace_sets.items():
            for trial_idx,single_trace in enumerate(traces.T):
                print('region=',region, 'trial=', trial_idx)
                if region not in file_results:
                    file_results[region] = {}
                
                if region in basal_data:
                    control_basal_std = basal_data[region]['std']
                    control_basal_mean = basal_data[region]['mean']
                        
                    auc_above, auc_below, dur_above, dur_below, drop_point_time, peak = diff_calc.analyze_traces(
                        time, single_trace, control_basal_mean, control_basal_std, region,ylbl=par+region+str(trial_idx),plot=plot_traces
                        )
                    file_results[region][trial_count[region]]={
                        "DropTime": drop_point_time,
                        "AUCabove": auc_above,
                        "AUCbelow": auc_below,
                        "IncrDur": dur_above,
                        "DecrDur": dur_below, #may not be accurate if there is a drop before and after the peak
                        "peak":peak
                    }
                else:
                    print('!!!!!!!!!!!!!!!!!!!!!! Region not in basal_data !!!!!!!!!!!!!!!!!!!!!!!')
                trial_count[region] += 1 

        results[par]=file_results
    tr_count=np.max(list(trial_count.values()))

    return results,tr_count

def do_calculations (traces_files,basal_files,mol,std_multiplier,params,thresh=None,regions=['dend','sa1']):
        baseline_time=[300 for f in traces_files] 
        onset_time=[300 if '4tr' in f else 500 for f in traces_files] #used to zero the baseline
        onset_dict=[{reg:ot for reg in regions} for ot in onset_time]
        for tr in params.tag_reg: #no change in dict if params.tag_reg=[]
            for ot in onset_dict:
                if params.tag_time:
                    ot[tr]=params.tag_time
                else: 
                    sp_regs,_,_=utils.spine_reg(pars)
                    ot[tr]=ot[sp_regs[0]]
        print('onset_dict, in do_calc',onset_dict)

        basal_data = utils.load_basal_means(params.dir, basal_files,regions=regions+params.tag_reg) #optional parameter: regions
        diff_calc = dc.DifferenceCalculator(std_multiplier,basal_data['dt'],params.norm,params.cutoff,regions,fixed_thresh=thresh)
        results,trial_count = process_files(params.dir, traces_files, basal_data, onset_dict,baseline_time,mol,diff_calc,regions=regions+params.tag_reg)

        return results,trial_count,diff_calc

ARGS="CK_PKA_Gi -keys  sig trials -dir resultsCKhalf2 -thresh 0.06 0.06 -remove 10u" #  -tag_reg sa1[1] sa1[2]"# -tag_time 300" #
#thresh: kinase: 0.06 0.07 (0.03 for dend, 10um) , CK_PKA_PAK: 0.09 0.1 (dend=0.05 for 10um), cof_act: 0.1 0.1 (dend=0.04 for 10um), CK_PKA_Gi:0.06 0.06 (dend=0.03 for 10um)
# 8. Process files and perform calculations
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
pars=utils.parse_args(args,do_exit)
output_filename=pars.dir.split('/')[-1]+'_'+'_'.join([str(t) for t in pars.thresh])

traces_keyword_sets=[[m]+pars.keys for m in pars.mols]
#regions=['dend','sa1[0]']#,'sa1[1]','sa1[2]']         
thresh={mol:{pars.reg[j]: float(pars.thresh[i*len(pars.reg)+j]) for j,reg in enumerate(pars.reg)} for i,mol in enumerate(pars.mols)}
if len(pars.tag_reg):
    output_filename+='multispine_'
    sp_regs,_,sp_name=utils.spine_reg(pars)
    sp_regs=[reg for reg in pars.reg if sp_name in reg]
    if len(sp_regs)==1:
        thresh_extra={mol:{tg:thresh[mol][sp_regs[0]] for tg in pars.tag_reg } for mol in pars.mols}
        for mol in thresh:
            thresh[mol].update(thresh_extra[mol])

#thresh={mol:{} for mol in pars.mols}  #uncomment this to use std_multiplier for threshold
std_multiplier = {'dend':2,'nonspine':2,'sa1[0]':2,'sa1[1]':2,'sa1[2]':2}  #empirical, larger for spine, not yet included in arg parser

for mol,traces_keywords in zip(pars.mols,traces_keyword_sets): 
    basal_keywords = traces_keywords+["basal"]
    traces_files = utils.search_files(pars.dir, traces_keywords)
    traces_files=utils.remove_files(traces_files,pars.dir,pars.remove,pars.keys)
    basal_files = utils.search_files(pars.dir, basal_keywords)
    basal_files=utils.remove_files(basal_files,pars.dir,pars.remove,pars.keys)
    if len(basal_files)==1:
        traces_files.remove(basal_files[0])
        print('traces',traces_files,'basal',basal_files)
        all_results,trial_count,difcalc=do_calculations (traces_files,basal_files[0],mol,std_multiplier,pars,thresh[basal_keywords[0]],regions=pars.reg)
    elif len(basal_files)>1: #if this works, perhaps can have all files in one directory?
        all_results={}
        for bas_fil in basal_files:
            prefix=bas_fil.split('basal')[0]  #verify basal is first keyword
            trace_fil=[f for f in traces_files if prefix in f]
            trace_fil.remove(bas_fil)
            print('BASAL file:', bas_fil, ', trace files:', trace_fil)
            results,trial_count,difcalc=do_calculations (trace_fil,bas_fil,mol,std_multiplier,pars,thresh[basal_keywords[0]],regions=pars.reg)
            all_results.update(results)
    else:
        print( ' no basal files found using',basal_keywords, 'in dir:',pars.dir)
    if len(traces_files):
        utils.save_results(all_results, output_filename,mol, trial_count, pars)
    else:
        print( ' no trace files found using',traces_keywords, 'in dir:',pars.dir)


"""
1. FIXME: onset_time from filename is problematic!
2. please go back and add more comments or else you might forget ohhh
3. include thresholds in output file names

"""