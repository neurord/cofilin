sub_species={'PKA':['PKA'],'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],
             'Rac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH','RCapGDP'],
             'actCof':['Cof','Cofactin'],'InCof':['pCof'],
             'totPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'],
             'totCofALL':['Cof','Cofactin','pCof','pLIMKCof','SSHpCof'],
             'totCof':['Cof','Cofactin','pCof'],
             'totRac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],
             'RacPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'],
             'CKtot':['KalCKCamCa4','KalCKpCamCa4','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1'],
             'CKonly':['CKp','CKCamCa4','CKpCamCa4'],
             'epac':['EpacAMP'],
             'LIMK':['RacPAKLIMK','PKAcLIMK','LIMK','pLIMK','pLIMKCof','SSHpLIMK'],
             'ssh':['CaNCamCa4pSSH','pSSH','SSH','SSHpLIMK','SSHpCof','RacPAKSSH','SCappSSH'],
             'Kal':['Kal','KalCKCamCa4','KalCKpCamCa4','KalPKAc','pKal','pKalPP1','pKalRac'],
             'phos':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi'],
             'PKAphos':['pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi','EpacAMP'],
             'phoslimk':['KalCKpCamCa4','pKal','pKalPP1','pKalRac','CKp','CKCamCa4','CKpCamCa4','CKpPP1','CKpCamCa4PP1','pPDE4','pPDE4cAMP','pLR', 'ppLR', 'ppLRGi','pLIMK','pLIMKCof','SSHpLIMK'],
             'dualPKA_PAK':{'pLIMK','pLIMKCof','SSHpLIMK'},
             'dualCK_PKA':{'pKal','pKalPP1','pKalRac'}}
##phos=pka and ck, 
tot_species=['RacPAK','totCofALL','totCof','actCof','dualCK_PKA','CKtot', 'PKAphos','dualPKA_PAK']# 'PKActot',
#tot_species=['CK','PKAc','ncx','pmca','PKAc','Cof','LIMK','SSH','ssh','Rac','Kal','PAK','Cam','CaN','PKAr','actin','Gap','CK','PP1','Ip35','AC1','AC8','PDE4','PDE1','Epac','Calbin']
weight={}
#signature molecules must be in tot_species or specified in -molx
signature={'kinase':{'num':['CKtot','PKAphos','EpacAMP'],'denom':[]}, 'CK_PKA_PAK':{'num':['CKtot','PKAphos','dualPKA_PAK','dualCK_PKA','EpacAMP'],'denom':[]},'cof_act':{'num':['actCof'],'denom':[]}} #,'CK_PKA':{'num':['CKtot','PKAphos','dualCK_PKA'],'denom':[]}
#thresh keys must be regions in the morphology
thresh={'kinase':{'dend':0.3,'dendsub':0.35,'sa1[0]':0.35},'CK_PKA_PAK':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.2},'cof_act':{'dend':0.15,'dendsub':0.15,'sa1[0]':0.2}} #'CK_PKA':{'dend':0.32,'dendsub':0.36,'sa1[0]':0.45},
min_max={}
min_max = {
    'kinase': {
        'num': {
            'CKtot': {
                'dend': {'max': 12763.348, 'min': 0.0},
                'dendsub': {'max': 1380.219, 'min': 0.0},
                'sa1[0]': {'max': 33514.489, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1828.008, 'min': 24.026},
                'dendsub': {'max': 411.554, 'min': 24.026},
                'sa1[0]': {'max': 1975.728, 'min': 22.677}
            },
            'EpacAMP': {
                'dend': {'max': 326.368, 'min': 0.963},
                'dendsub': {'max': 345.081, 'min': 0.0},
                'sa1[0]': {'max': 397.703, 'min': 0.0}
            }
        },
        'denom': {}
    },
    'CK_PKA_PAK': {
        'num': {
            'dualPKA_PAK': {
                'dend': {'max': 1790.033, 'min': 60.039},
                'dendsub': {'max': 209.124, 'min': 56.562},
                'sa1[0]': {'max': 1983.401, 'min': 33.696}
            },
            'dualCK_PKA': {
                'dend': {'max': 477.719, 'min': 0.0},
                'dendsub': {'max': 315.295, 'min': 0.0},
                'sa1[0]': {'max': 7093.44, 'min': 0.0}
            },
            'CKtot': {
                'dend': {'max': 12763.348, 'min': 0.0},
                'dendsub': {'max': 1380.219, 'min': 0.0},
                'sa1[0]': {'max': 33514.489, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1828.008, 'min': 24.026},
                'dendsub': {'max': 411.554, 'min': 24.026},
                'sa1[0]': {'max': 1975.728, 'min': 22.677}
            },
            'EpacAMP': {
                'dend': {'max': 326.368, 'min': 0.963},
                'dendsub': {'max': 345.081, 'min': 0.0},
                'sa1[0]': {'max': 397.703, 'min': 0.0}
            }
        },
        'denom': {}
    },
    'cof_act': {
        'num': {
            'actCof': {
                'dend': {'max': 1306.338, 'min': 15.983},
                'dendsub':  {'max': 147.269, 'min': 8.614},
                'sa1[0]': {'max': 2512.819, 'min': 4.93}
            }
        },
        'denom': {}
    }
}


if __name__ == '__main__':
    for key in signature.keys():
        if key in min_max:
            for nd in ['num','denom']:
                for mol in signature[key][nd]:
                    if not mol in min_max[key][nd]:
                        print('key=',key,', mol',mol,'in sig, not in min_max[key][',nd,']')
        else:
            print('key=',key,'in signature, not in min_max - norm signature will fail')
        if key not in thresh.keys():
            print('key=',key,'in signature dict, missing from thresh dictionary')
    for key in thresh.keys():
        if key not in signature.keys():
            print('key=',key,'in thresh dict, missing from sig - plot_signature will fail')
                    
