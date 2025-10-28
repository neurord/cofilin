sub_species={'PKA':['PKA'],'PKAr':['PKA','PKAr','PKAcAMP2','PKAcAMP4'],
             'PKAc':['PKAc','KalPKAc','PKAcLIMK','PKAc_PDE4_cAMP','PKAcPDE4','PKAcLR','PKAcpLR','PKAcppLR'],
             'Rac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH','RCapGDP'],
             'actCof':['Cof','Cofactin'],'InCof':['pCof'],
             'totPAK':['RacPAK','RacPAKLIMK','RacPAKSSH'],
             'totCofALL':['Cof','Cofactin','pCof','pLIMKCof','SSHpCof'],
             'totCof':['Cof','Cofactin','pCof'],
             'totRac':['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH'],
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
tot_species=['actCof','CKtot','PKAphos','phoslimk','dualPKA_PAK','dualCK_PKA']#'totactCof'#
#tot_species=['CK','PKAc','ncx','pmca','PKAc','Cof','LIMK','SSH','ssh','Rac','Kal','PAK','Cam','CaN','PKAr','actin','Gap','CK','PP1','Ip35','AC1','AC8','PDE4','PDE1','Epac','Calbin']
weight={}
#signature molecules must be in tot_species
signature={'kinase':{'num':['CKtot','PKAphos'],'denom':[]}, 'CK_PKA_PAK':{'num':['CKtot','PKAphos','dualPKA_PAK','dualCK_PKA'],'denom':[]},'cof_act':{'num':['actCof'],'denom':[]}} #,'CK_PKA':{'num':['CKtot','PKAphos','dualCK_PKA'],'denom':[]}
#thresh keys must be regions in the morphology
thresh={'kinase':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.2},'CK_PKA_PAK':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.3},'cof_act':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.3}} #,'CK_PKA':{'dend':0.2,'dendsub':0.2,'sa1[0]':0.3}
min_max={}
min_max = {
    'kinase': {
        'num': {
            'CKtot': {
                'dend': {'max': 12689.75, 'min': 0.0},
                'dendsub': {'max': 1354.42, 'min': 0.0},
                'sa1[0]': {'max': 33935.21, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1834.69, 'min': 20.86},
                'dendsub': {'max': 411.139, 'min': 20.86},
                'sa1[0]': {'max': 2069.08, 'min': 20.70}
            }
        },
        'denom': {}
    },
    'CK_PKA_PAK': {
        'num': {
            'dualPKA_PAK': {
                'dend': {'max': 1873.92, 'min': 104.92},
                'dendsub': {'max': 221.58, 'min': 94.96},
                'sa1[0]': {'max': 2193.12, 'min': 93.04}
            },
            'dualCK_PKA': {
                'dend': {'max': 324.64, 'min': 0.0},
                'dendsub': {'max': 214.21, 'min': 0.0},
                'sa1[0]': {'max': 6436.14, 'min': 0.0}
            },
            'CKtot': {
                'dend': {'max': 12689.75, 'min': 0.0},
                'dendsub': {'max': 1354.42, 'min': 0.0},
                'sa1[0]': {'max': 33935.21, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1834.69, 'min': 20.86},
                'dendsub': {'max': 411.139, 'min': 20.86},
                'sa1[0]': {'max': 2069.08, 'min': 20.70}
            }
        },
        'denom': {}
    },
    'cof_act': {
        'num': {
            'actCof': {
                'dend': {'max': 629.78, 'min': 3.79},
                'dendsub': {'max': 76.07, 'min': 2.91},
                'sa1[0]': {'max': 2145.81, 'min': 2.91}
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
                    
