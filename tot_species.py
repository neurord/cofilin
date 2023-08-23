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
sub_species={'PKA':['PKA'],'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],'actCof':['Cof','Cofactin'],'InCof':['pCof'],'totPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'], 'totCof':['Cof','Cofactin','pCof','SSHpCof','pLIMKCof'],'totRac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],'CKp':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1'],'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR']}

tot_species=['totRac','totCof','actCof','CKp','PKAc']#['ncx','pmca','PKAc','Cof','LIMK','SSH','Rac','Kal','PAK','Cam','CaN','PKAr','actin','Gap','CK','PP1','Ip35','AC1','AC8','PDE4','PDE1','Epac','Calbin']#
weight={}
#signature molecules must be in tot_species
signature={'kinase':{'num':['CKp','PKAc'],'denom':[]}, 'cof':{'num':['actCof'],'denom':['pCof']}}
#thresh keys must be regions in the morphology
thresh={'dend':0.1,'sa1[0]':0.2}


 
