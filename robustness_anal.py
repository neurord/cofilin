#in python exec(open('path/to/file/robustness_anal.py')
##DO NOT PUT ANY SPACES NEXT TO THE COMMAS, DO NOT USE TABS
#find_filename is the specific file name that needed to be replaced or update initial concentration (here is the IC), change if needed 
#suffix_name is the specific tag name find in the files, 2 options given here, either random or set
#input_filename is the initial model filename, define as set of file


import glob
import sys
import importlib
import robustness_functions as rf
##############################################

prog_path_name='/local/vol00/Users/klblackwell/neurord-3.3.0-all-deps.jar'
###################################################################################set up args#####
ARGS='rand -model Model_Cof-basalctrlATP -change mol_change -frange 20 -start 0 -prog ss -outdir robust1/'
ARGS='rand -model Model_Cof-basalctrlATP -change mol_change -frange 20 -start 20 -prog ss -outdir robust2/'
#ARGS='rand -model Model_Cof-basalctrlATP -change mol_change -frange 20 -start 40 -prog ss -outdir robust3/'
#ARGS='rand -model Model_Cof-basalctrlATP -change mol_change -frange 20 -start 60 -prog ss -outdir robust4/'
#ARGS='set -model Model_Cof_10um3spines-4trains_massedtag -modeldir Exp_10um_3spines/ -change mol_change_set -factor 0.1'
try:
    args = ARGS.split(" ")
    print("ARGS =", ARGS, "commandline=", args)
    do_exit = False
except NameError: #NameError refers to an undefined variable (in this case ARGS)
    args = sys.argv[1:]
    print("commandline =", args)
    do_exit = True

try:
    data.close()
except Exception:
    pass

#read parameters and assign variable names
pars=rf.parse_args(args,do_exit)
change_file=importlib.import_module(pars.change)
mol_change=change_file.sub_species
if pars.prog=='neurord':
    text='java -jar  '+prog_path_name+' '+'-Dneurord.trials=5 '+'-t 3600000'#update for desire textline
elif pars.prog=='ss':
    text='steadystate'
else:
    print('unknown program')

main_path=pars.dir
if main_path.endswith('/') and pars.modeldir=='/':
    model_path=main_path
else:
    model_path=main_path+pars.modeldir #e.g. cof/Exp_3spines/
ICfile=pars.ICfile#+'.xml'
find_ICfile=main_path+ICfile #full path to IC file
frange=pars.frange #number of random variation sims
suffix_name=pars.modtype
if not pars.outdir.endswith('/'):
    pars.outdir+='/'
output_path=main_path+pars.outdir #cof/robust1/
if output_path==main_path:
    print('model files being placed in main directory')
elif model_path.count('/')==output_path.count('/'): #model files won't work otherwise since xml files may be specified with ../
    print('model files being placed in output directory with IC files')
elif output_path==model_path:
    print('model files being placed directory with top level model files')
else:
    print('model files being placed in output directory, but may not run properly')

########## create new IC files with random variations
if suffix_name=='rand':
    ICfileNames=rf.random_file(output_path,frange,find_ICfile,mol_change,start=pars.start)
else:
    ICfileNames=rf.set_file(output_path,find_ICfile,pars.factor,mol_change)

#create new model file(s) for each new IC file
pattern_mod=model_path+pars.model+'.xml'
model_filename=sorted(glob.glob(pattern_mod)) #set of files
fileNames_batch=rf.modelrobust_file(ICfileNames,model_filename,find_ICfile,output_path,pars.prog)

if pars.outdir[-2].isdigit():
    suffix_name+=pars.outdir[-2]
rf.bat_file(text,fileNames_batch,suffix_name,pars.prog)

####################
## Next steps:
## 6. read in params and pCof and analyze with discriminant analysis (analyze_json.py, analyze_robust_results.py)
## 7. select a subset of params and run sims (robustness_anal.py using prog=neurord)
##      edit Model files to remove extra params OR, input IC files and orig Model files and generate new Model files (simpler prog##      those with largest basal change - two biggest in opposite directions, next two biggest
##      which stim files? massed tagging, test with RF
