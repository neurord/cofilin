sub_species={
            'set1':{('totRac',):['pKalRac','RacGap','RacGDP','RacGTP','RacPAK','RacPAKLIMK','RacPAKSSH','RCapGDP'],
                    ('totCof',-0.1):['Cof','Cofactin','pCof','pLIMKCof','SSHpCof']},
            'set2':{('LIMKtot',0.1):['RacPAKLIMK','LIMK','pLIMK','pLIMKCof','SSHpLIMK'],
                    ('Kal',-0.1):['Kal','KalCKCamCa4','KalCKpCamCa4','pKal','pKalPP1','pKalRac']},
            }
#either make key a tuple, or make list of molecules entry into dict and add factor to the dict.
#omit fac
