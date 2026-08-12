import glob
import os
from lxml import etree
from xml.etree import ElementTree as ET
import numpy as np

def parse_args(commandline,do_exit):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('modtype',type=str,choices=['rand','set'],help='type of parameter variations,rand:randomly change all, set: single factor changes') 
    parser.add_argument('-prog',type=str,choices=['neurord','ss'],help='type of sim: neurord or steadystate',default='neurord') 
    parser.add_argument('-dir', type=str, help = 'Main path, must contain IC file',default='/local/vol00/Users/klblackwell/sigpath/cofilin/')
    parser.add_argument('-modeldir', type=str, help = 'subdirectory with model files, specify "/" if same as Main path', default='robust/')
    parser.add_argument('-outdir', type=str, help = 'subdirectory with model files', default='robust/')
    parser.add_argument('-ICfile', type=str, help = 'name of IC files to change', default='IC_Cof_ctrl_oldCamh5_updateI1PKA')
    parser.add_argument('-model', type=str, help = 'name of Model files to change', default='')
    parser.add_argument('-change', type=str, help = 'name of python file with sets of molecules to change IC', default='mol_change.py')
    
    parser.add_argument('-frange',type=int,help='number of random variations to do', default=1 )
    parser.add_argument('-start',type=int,help='starting number for labeling output files', default=0 )
    parser.add_argument('-factor',type=float,help='fractional change in params for set', default=0.1 )
    try:
        args = parser.parse_args(commandline) # maps arguments (commandline) to choices, and checks for validity of choices.
        #if arguments are mapped incorrectly, python wants to exit, but the next line says "don't", instead check whether we are in python (do_exit=False) then don't exit, just give us a warning
    except SystemExit:
        if do_exit:
            raise # raise the exception above (SystemExit) b/c none specified here
        else:
            raise ValueError('invalid ARGS')
    return args


def random_file(oPath,frange,find_ICfile,mol_change,start=0):
    #create set of IC files which have random variations in parameters
    import pandas as pd
    from datetime import datetime #use date_string in filename of random changes
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    find_name=os.path.basename(find_ICfile) #find the ctrl ICfile starting point
    all_change_rows={}
    all_IC_files=[]
    for i in range(frange):
        outfile=oPath+find_name+'-random'+str(i+start)+'.xml' #output filename
        root=ET.parse(find_ICfile+'.xml').getroot() #read in original ICfile
        change_row={} #accumulate list of parameter changes
        for mol in mol_change.keys(): #mol_change has dict of molecules to change, with subspecies
            change=np.random.uniform(.9,1.1) #apply same change to all instances of all forms of the molecule
            change_row[mol]=round(change,4) 
            for molecules in mol_change[mol]: 
                #change=np.random.uniform(.9,1.1) #apply same change to all instances of the molecule
                for elem in root: #find the molecules in xml file that should be changed
                    for subelem in elem:
                        if molecules== subelem.attrib['specieID']:
                            oldval=float(subelem.attrib['value'])
                            newval=str(round(change*oldval,4))  #calculate new value
                            subelem.attrib['value']=newval  #assign new value
        all_change_rows[str(i+start)]=change_row #add the set of new values to dictionary
        with open(outfile, 'wb') as out: #write the new xml file
            out.write(ET.tostring(root))
        all_IC_files.append(outfile) #list of IC files
    df = pd.DataFrame(all_change_rows).transpose() #create dictionary with changes to write csv file
    df.to_csv(oPath+'random_change_file'+date_string+'.csv', index_label='index') 
    return all_IC_files

def set_file(oPath,find_filename,factor,mol_change):
    #create set of IC files which have single molecule(s) change (by specified factor)
    factor=1+factor #multiplicative factor for set change
    root=ET.parse(find_filename+'.xml').getroot()
    find_name=os.path.basename(find_filename)
    all_IC_files=[]
    for molset in mol_change.keys(): #e.g., set1
        for mol_fac in mol_change[molset].keys(): #tuple of molecule, factor (or just molecule), e.g. totRac or totCof
            mol=mol_fac[0]
            if len(mol_fac)>1:
                fac=1+mol_fac[1] #use molset specific factor, can be negative
            else:
                fac=factor #just use command line factor+1
            for molecules in mol_change[molset][mol_fac]: #list of molecule forms
                for elem in root:
                    for subelem in elem:
                         if molecules== subelem.attrib['specieID']:
                            oldval=float(subelem.attrib['value'])
                            newval=str(oldval*fac)
                            subelem.attrib['value']=newval
        outfile=oPath+find_name+'-set'+mol+str(fac)+'.xml'
        with open(outfile, 'wb') as out:
            out.write(ET.tostring(root))
        all_IC_files.append(outfile)
    return all_IC_files

############################ create model file with replace one line ######################################
def modelrobust_file(newIC_files,model_filenames,orig_ICfile,output_path,prog):
    #create the top level model files - one for each new IC file
    all_modl_files=[]
    for replace in newIC_files: #list of new IC files
        print('model, IC=',replace,all_modl_files)
        replace_filename=os.path.basename(replace)
        newICdir=os.path.dirname(replace)
        orig_IC=os.path.basename(orig_ICfile)
        for modl_file in model_filenames: #name of model files
            new_fname=replace_filename.split('-')[-1]
            if prog=='ss':
                new_fname='ss-'+new_fname
            #construct the output Model filename, using change in IC file name
            out_filename=output_path+os.path.splitext(os.path.basename(modl_file))[0]+'-'+new_fname
            input=open(modl_file,'r') #open the input file
            output=open(out_filename,'w')#open the model file
            #print('model=',modl_file,', new IC=',replace_filename,'output',out_filename,'orig_IC=',orig_IC)
            for line in input: #read Model file line by line
                if orig_IC in line: #fine the line with IC file in it
                    spaces=line.find('<')
                    line=' '*spaces+'<xi:include href="'+newICdir+'/'+replace_filename+'" />\n' #construct new line
                output.write(line) #write new model file line by line
                if '<calculation>' in line:  #place new parameters for steadystate after calculation and before  /SDRun                 
                    if prog=='ss':
                        line='    <absTolerance>     1e-5  </absTolerance>\n    <iterations>     100    </iterations>\n'
                        output.write(line)
            #close both files before doing the next file
            input.close()
            output.close()
            all_modl_files.append(out_filename)
    return all_modl_files


##################################### create batch file #############################3
def bat_file(text,fileNames_batch,suffix_name,prog):
    outfname=suffix_name+'_'+prog+'.bat'
    f=open(outfname,'w')
    if prog=='ss': #how to activate the environment - commented out since doesn't work in .bat file
        textline='#source /iahome/k/kl/klblackwell/python/sscalculation/.venv/bin/activate\n'
        f.write(textline)
    for files in fileNames_batch:
        textline=text+' '+files+'\n' #write one line for each simulation, use full path to model file
        print(textline)
        f.write(textline)
    f.write('#deactivate\n')
    f.close()
#################################################################
