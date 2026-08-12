===========
**Model files for simulating the cofilin signaling pathway underlying hippocampal LTP**
===========

*Signaling pathways include*: 

    1. Calcium influx through the NMDA receptor leading to activation of AC1 and AC8, calcineurin, CaMKII  

    2. Norepinephrine, Beta-androgenic receptor, couple to G protein leading to an increase of cAMP, thus PKA activation  

    3. Cofilin activation via Ca/CaMKII and cAMP/PKA: Rac, PAK, SSH and LIMK 

   .. figure:: https://github.com/neurord/cofilin/blob/master/Cofilin_diagram.jpg
        :alt: ERK signaling pathwway diagram
        :figclass: align-center 
    
    **Figure: Schematic representation of signaling pathways activating Cofilin**
    

 **Note**: *1 and 2 are (from published model (Jȩdrzejewska-Szmek, J., Luczak, V., Abel, T., Blackwell, K.T., 2017. β-adrenergic signaling broadly contributes to LTP induction. PLOS Computational Biology 13, e1005657.)* 

Model_Cofxxx.xml contains the entire model specification, which combines Reaction file (*Rxn_Cof*.xml*), Morphology file (*Morph*.xml*), initial conditions file (*IC_Cof*.xml*), output file (*Out_Cof*.xml*) and stimulation (*Stim_Cof*.xml*). To run simulations, use NeuroRDv3.3.0: 

 	`java -jar /path/to/neurord-3.2.4-all-deps.jar /path/to/Modelfile.xml`

 All output files were first processed using nrdh5_analv2 in https://github.com/neurord/NeuroRDanal 

**Main folder**: Reaction files, stimulation files and Morphology files and updated IC files used in all simulation. 
-------------
 Subfolders: 
-------------
 **Init:** 

    1. To determine steady state / initial basal concentrations, simulate the model for about an hour to obtain in the absence of stimulation 

    2. To copy basal quantities of molecules, run: ARGS="h5_filename -sstart ssend -IC IC_filename -Rxn Rxn_filename -tot tot_species_filename" (-tot is optional) 

    then exec(open('path/to/file/UpdateIC_basal_spatial.py').read()) 

**Init**: Model files for spatial simulation in 1 spine model, without stimulation, to determine steady state initial conditions

**Exp_1spine**: Model files for simulation with 2 um long dendrite with 1 spine

**Exp_10um_3spines**: Model files for spatial simulation with 10 um long dendrite with 3 spines 

The Model reaction kinetics and molecule quantities are summarized in Cofilin_parameters.xls. 

----------------------------------
 Analysis of nrdh5_analV2 output: 
----------------------------------
**dataset_analysis:** 

    read in output of nrdh5_analV2.py and extract features
    
    parameters are
    
        molecule name
        
        -key: keywords that uniquely specify a set of files, should include the word trials 
        
        -dir: directory containing the files
        
        -thresh: threshold for each region
        
        -reg: regions to analyze, default = ['dend','sa1[0]']
        
        -tag_reg: For tagging simulations, name of other spines to analyze
        
        -tag_time: if weak stimulation is provided, time after which to analyze the other spines

**StatAnalCof:**

    read in the output of dataset_analysis and perform Random Forest Regression
    
    parameters (edit at top of __main__) are:
    
        file_dict: training and testing files.  If test files are separated from training files, can specifiy the parameter considered controls.  If two files are specified for training or testing, the files are merged according to training parameter
        
        ycol: name of column which has outcome, either 0 or 1, of protocol.  Must be added manually to one of each of training and testing files
        
        regions: names of regions.  For spines, only specify the spine name, not number.  E.g. sa1, not sa1[0]
        
        regtype: whether to do regression, cluster analysis, or both

        
