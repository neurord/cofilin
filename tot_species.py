sub_species={'PKA':['PKA'],'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKActot':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],
             'Rac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'totRac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH','RCapGDP'],
             'actCof':['Cof','Cofactin'],'InCof':['pCof'],
             'totPAK':['PAK','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'RacPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'],
             'totCofALL':['Cof','Cofactin','pCof','pLIMKCof','SSHpCof'],
             'pCoftot':['pCof','SSHpCof'],
             'CKtot':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1'],
             'CKonly':['CKp','CKCamCa4','CKpCamCa4'],
             'LIMKtot':['RacPAKLIMK','PKAcLIMK','LIMK','pLIMK','pLIMKCof','SSHpLIMK'],
             'LIMKall':['RacPAKLIMK','PKAcLIMK','LIMK'],
             'pLIMKall':['pLIMK','pLIMKCof','SSHpLIMK'],
             'ssh':['CaNCamCa4pSSH','pSSH','SSH','SSHpLIMK','SSHpCof','RacPAKSSH','SCappSSH'],
             'Kal':['Kal','KalCKCamCa4','KalCKpCamCa4','KalPKAc','pKal','pKalPP1','pKalRac'],
             'phos':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi'],
             'PKAphos':['pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi'],#'EpacAMP'],
             'phoslimk':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi','pLIMK','pLIMKCof','SSHpLIMK'],
             'dualPKA_PAK':['pLIMK','pLIMKCof','SSHpLIMK'],
             'dualCK_PKA':['pKal','pKalPP1','pKalRac'],
             'Gs':['GsR', 'LRGs','Gs', 'Gsbg'],
             'R':['R','LR','GsR','LRGs','pLR'],
             'GasGTP':['GasGDP', 'GasGTP','AC1GasGTP','AC1GasGTPCamCa4','AC1GasGTPCamCa4ATP'],
             'PP1':['PP1','Ip35PP1', 'pKalPP1']}
##phos=pka and ck, 
tot_species=['dualPKA_PAK','pCoftot','PKAphos','CKonly','dualCK_PKA','pLIMKall','RacPAK','totCofALL','actCof','CKtot']# 'PKActot',
#tot_species=['CK','totCofALL','LIMKtot','ssh','totRac','Kal','totPAK','CaN','Ng','PKAr','PKActot','actin','Gap','CK','PP1','Ip35','PDE4','Epac','Calbin', 'AC8', 'AC1', 'Gs','R','GasGTP','RCap','SCap', 'PP1'] #sum molecules to ensure totals are correct
#tot_species=['pCoftot','pLIMKall','LIMKall']
weight={}
#signature molecules must be in tot_species or in molecules
signature={'kinase':{'num':['CKtot','PKAphos','EpacAMP'],'denom':[]}, 'CK_PKA_PAK':{'num':['CKtot','PKAphos','dualPKA_PAK','dualCK_PKA'],'denom':[]},'CK_PKA':{'num':['CKtot','PKAphos','dualCK_PKA','EpacAMP'],'denom':[]},'cof_act':{'num':['actCof'],'denom':[]}}
#thresh keys must be regions in the morphology
thresh={'kinase':{'dend':0.4,'dendsub':0.45,'sa1[0]':0.45},'CK_PKA_PAK':{'dend':0.22,'dendsub':0.22,'sa1[0]':0.22},'CK_PKA':{'dend':0.32,'dendsub':0.36,'sa1[0]':0.45},'cof_act':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.3}}
#signature={}
#thresh={}
min_max={}   
