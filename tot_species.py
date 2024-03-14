
'''
sub_species={'Kal':['Kal','KalCKCamCa4','KalCKpCamCa4','KalPKAc','pKal','pKalPP1','pKalRac'],
             'RacGDP':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'Gap':['RacGap','Gap'],'PAK':['PAK','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'LIMK':['RacPAKLIMK','PKAcLIMK','LIMK','pLIMK','pLIMKCof','SSHpLIMK'],
             'SSH':['CaNCamCa4pSSH','pSSH','SSH','SSHpLIMK','SSHpCof','RacPAKSSH'],
             'Cof':['Cof','pCof','pLIMKCof','SSHpCof','Cofactin'],'actin':['Cofactin','actin'],
             'Ca':['KalCKCamCa4','KalCKpCamCa4','CamCa2C','CamCa2N','CaNCamCa2C','CaNCamCa2N','CaNCamCa4','CaNCamCa4pSSH','CamCa4','CKCamCa4','CKpCamCa4','CKpCamCa4PP1','pmcaCa','ncxCa','CalbinC','AC1GasGTPCamCa4','AC1GasGTPCamCa4ATP','AC1CamCa4','AC1CamCa4ATP','AC8CamCa4','AC8CamCa4ATP','PDE1CamCa4','PDE1CamCa4cAMP'],
             'PKA':['PKA','PKAc','PKAr','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR','PKAcAMP2','PKAcAMP4'],
             'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],
             'cAMP':['cAMP','PDE4cAMP','pPDE4cAMP','PKAc_PDE4_cAMP','PKAcAMP2','PKAcAMP4'],
             'Cam':['Cam','CamCa2C','CamCa2N','CaNCam','CaNCamCa2C','CaNCamCa2N','CaNCamCa4','CaNCamCa4pSSH','CamCa4','CKCamCa4','CKpCamCa4','CKpCamCa4PP1','KalCKCamCa4','KalCKpCamCa4','NgCam','AC1GasGTPCamCa4','AC1GasGTPCamCa4ATP','AC1CamCa4','AC1CamCa4ATP','AC8CamCa4','AC8CamCa4ATP'],
             'CKp':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1'],
             'CaN':['CaN','CaNCam','CaNCamCa2C','CaNCamCa2N','CaNCamCa4','CaNCamCa4pSSH'],
             'PP1':['Ip35PP1','PP1','CKpPP1','CKpCamCa4PP1','pKalPP1'],'Ip35':['Ip35','Ip35PP1'],
             'AC1':['AC1','AC1GasGTP','AC1GasGTPCamCa4','AC1GasGTPCamCa4ATP','AC1CamCa4','AC1CamCa4ATP'],'AC8':['AC8','AC8CamCa4','AC8CamCa4ATP'],
             'PDE4':['PDE4','PDE4cAMP','PKAcPDE4','pPDE4','pPDE4cAMP','PKAc_PDE4_cAMP'],
             'PDE1':['PDE1','PDE1CamCa4','PDE1CamCa4cAMP']}
'''
'''
sub_species={'PKA':['PKA'],'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],
             'PKAt':['pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi'],
             'actCof':['Cof','Cofactin'],'InCof':['pCof'],
             'totPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'],
             'totCof':['Cof','Cofactin','pCof','SSHpCof','pLIMKCof'],
             'totRac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'CKp':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1'],
             'CK':['CKp','CKCamCa4','CKpCamCa4'],
             'epac':['EpacAMP'],
             'LIMK':['RacPAKLIMK','PKAcLIMK','LIMK','pLIMK','pLIMKCof','SSHpLIMK'],
             'SSH':['CaNCamCa4pSSH','pSSH','SSH','SSHpLIMK','SSHpCof','RacPAKSSH'],
             'Kal':['Kal','KalCKCamCa4','KalCKpCamCa4','KalPKAc','pKal','pKalPP1','pKalRac'],
             'phos':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi'],
             'phoslimk':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi','pLIMK','pLIMKCof','SSHpLIMK']}
'''
sub_species={'Rac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH','RCapGDP']}
tot_species=['LIMK','SSH','Kal','CK','Epac','CK','ncx','pmca','Cof','LIMK','SSH','Rac','Kal','PAK','Cam','CaN','actin','Gap','PP1','Ip35','AC1','AC8','PDE4','PDE1','Calbin']
#tot_species=['totCof','actCof','InCof','epac','PKAt','CKp','CK','phoslimk','phos']
weight={}
#signature molecules must be in tot_species
signature={'kinasePKAphos':{'num':['CKp','PKAc','epac'],'denom':[]},'kinasephos':{'num':['phos','epac'],'denom':[]},'kinasephoslimk':{'num':['phoslimk','epac'],'denom':[]},'product':{'num':['actCof','CK'],'denom':[]}}#}, 'kali':['Kal']}#, 'inactivecof':{'num':['InCof'],'denom':[]}}'ratiocof':{'num':['actCof'],'denom':['InCof']},'cof':{'num':['actCof'],'denom':[]},'totalcof':{'num':['totCof'],'denom':[]},
#thresh keys must be regions in the morphology.  Possibly different thresh for each "mol"?
thresh={'kinasePKAphos':{'dend':0.1,'dendsub':0.1,'neck':0.1,'sa1[0]':0.1},'kinasephos':{'dend':0.1,'dendsub':0.1,'neck':0.1,'sa1[0]':0.1},'kinasephoslimk':{'dend':0.1,'dendsub':0.1,'neck':0.1,'sa1[0]':0.1},'product':{'dend':0.1,'dendsub':0.1,'neck':0.1,'sa1[0]':0.1}}#,'kali':{'dend':0.1,'sa1[0]':0.1}} 'ratiocof':{'dend':0.1,'sa1[0]':0.1},'cof':{'dend':0.1,'sa1[0]':0.2},'totalcof':{'dend':0.1,'sa1[0]':0.1},



 
