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
                'dend': {'max': 15763.796584706137, 'min': 0.8302693915813638},
                'dendsub': {'max': 1684.8241628664823, 'min': 0.0},
                'sa1[0]': {'max': 31199.881689536902, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1514.2981516910081, 'min': 16.812955179522614},
                'dendsub': {'max': 375.48933234267525, 'min': 13.595661287140112},
                'sa1[0]': {'max': 1634.2916960090529, 'min': 13.28431026530418}
            }
        },
        'denom': {}
    },
    'CK_PKA_PAK': {
        'num': {
            'dualPKA_PAK': {
                'dend': {'max': 1897.6687533340682, 'min': 88.09431851204957},
                'dendsub': {'max': 223.7576010311775, 'min': 87.90477183367689},
                'sa1[0]': {'max': 2222.5344034927098, 'min': 87.90477183367689}
            },
            'dualCK_PKA': {
                'dend': {'max': 506.33853047196715, 'min': 0.0},
                'dendsub': {'max': 334.28721378544657, 'min': 0.0},
                'sa1[0]': {'max': 7324.900496666423, 'min': 0.0}
            },
            'CKtot': {
                'dend': {'max': 15763.796584706137, 'min': 0.8302693915813638},
                'dendsub': {'max': 1684.8241628664823, 'min': 0.0},
                'sa1[0]': {'max': 31199.881689536902, 'min': 0.0}
            },
            'PKAphos': {
                'dend': {'max': 1514.2981516910081, 'min': 16.812955179522614},
                'dendsub': {'max': 375.48933234267525, 'min': 13.595661287140112},
                'sa1[0]': {'max': 1634.2916960090529, 'min': 13.28431026530418}
            }
        },
        'denom': {}
    },
    'cof_act': {
        'num': {
            'actCof': {
                'dend': {'max': 657.4538496594083, 'min': 2.3870245007964206},
                'dendsub': {'max': 79.29072689602023, 'min': 2.3870245007964206},
                'sa1[0]': {'max': 2097.213131028794, 'min': 0.9340530655290344}
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
                    
