import numpy as np
import operator
import RandForstUtils as RFU
import pandas as pd 
import re

def lin_reg(X_train, X_test, y_train, y_test, variables,label_train,label_test):
    from sklearn.feature_selection import f_regression
    from scipy.stats import pearsonr

    RFU.run_glm(X_train,y_train,X_test,y_test,variables,'RFreg',label_test)
    #evaluate which features are correlated with each other
    corr_dict={var:{} for var in X_train.columns}
    for col1, var1 in enumerate(X_train.columns):
        for col2,var2 in enumerate(X_train.columns):
            corr_coef, p_value = pearsonr(X_train[var1],X_train[var2])
            corr_dict[var1][var2]=(corr_coef,p_value)
            #if col2>col1:
            #    print(var1,var2,corr_coef,p_value)

    #### Predict which features would be good from f_fregression
    pvalfeat=[]
    print('\nPredict features from f_regression - single variable at a time')
    F = f_regression(X_train, y_train, center=True)
    for feat, pval in zip(X_train.columns, F[1]):
        pvalfeat.append((pval,feat))
    #select top features from above, as long as not highly correlated with another feature:    
    sortedpval=sorted(pvalfeat)
    statsmol=[]
    for pval,feat in sortedpval:
        print('   feature: {}, pvalue: {}'.format(feat,pval))
        if len(statsmol): #is the next feature correlated with previous feature?
            xcorr=sorted([corr_dict[feat][sm] for sm in statsmol], reverse=True)
        else:
            xcorr=[[0,1]]
        if xcorr[0][1]> .005 and (pval<0.1 or len(statsmol)<3): #use 3, or more than 3 if highly significant
            if len(statsmol): 
                print('   FYI, correlation with prior features {} = {}'.format(statsmol,xcorr))
            statsmol.append(feat)
        elif len(statsmol)>0 and len(statsmol)<3:
            print('   NOT INCLUDING due to correlation with prior features {} = {}'.format(statsmol,xcorr))

    RFU.run_glm(X_train,y_train,X_test,y_test,statsmol,'f_regression - single variable at a time',label_test)   
 
def runClusterAnalysis(X_train, X_test, y_train, y_test,max_feat,n_estim,epoch,ylabels,best_score,x_unk=[],label_unk=[],incorrect=True):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
    from sklearn import tree
    from matplotlib import pyplot as plt
    train_test = {'train':(X_train,y_train), 'test':(X_test, y_test)}
    rtc = RandomForestClassifier(n_estimators=n_estim, max_features=max_feat)

    #This line actually builds the random forest (does the training)
    rtc.fit(X_train,y_train)

    ###### EVALUATE THE RESULT      
    predict_dict,conf_matrix,accuracy=RFU.score(train_test,rtc)
    #evauate the importance of each feature in the classifier
    #The relative rank (i.e. depth) of a feature used as a decision node in a tree can be used to assess the relative importance of that feature with respect to the predictability of the target variable. 
    feature_order = sorted({feature : importance for feature, importance in zip(list(X_train.columns), list(rtc.feature_importances_))}.items(), key=operator.itemgetter(1), reverse=True)
    
    ###### 3d, plot amd print the predictions of the actual data -- you can do this if # of epochs is low
    if accuracy['test']>best_score:
        best_score=accuracy['test']
        RFU.plotPredictions(max_feat, train_test, predict_dict, feature_order,epoch,accuracy)
        RFU.print_predict(y_test,predict_dict,ylabels,accuracy['test'],incorrect_only=incorrect,label_unk=label_unk)
        RFU.conf_matrix_plot(conf_matrix,title='RF Cluster')
        for i in range(2): #plot three estimators
            treed = rtc.estimators_[i]
            plt.figure(figsize=(15,8))
            what=tree.plot_tree(treed,feature_names = X_train.columns, filled=True, fontsize=6, rounded = True)
    #print('epoch {} best features {}'.format(epoch,feature_order[0:max_feat]))
    return feature_order[0:max_feat],best_score

def start_clusterAnal(X_train, X_test, y_train, y_test,epochs,ylabels,x_unknown=[],label_unk=[]):
    max_feat=int(np.ceil(np.sqrt(len(X_train.columns))))
    n_estim=10

    collectionBestFeatures = {}
    collectionTopFeatures = {}
    best_score=0
    for epoch in range(0, epochs):
        features,best_score = runClusterAnalysis(X_train, X_test, y_train, y_test,max_feat,n_estim,epoch,ylabels,best_score,x_unknown,label_unk,incorrect=True)
        #pass in parameter to control plotting
        #print('######### BEST FEATURES for EPOCH '+str(epoch)+' #######')
        for i,(feat, weight) in enumerate(features):
            #print(i,feat,weight) #monitor progress 
            if feat not in collectionBestFeatures:          # How is the weight scaled? caution
                collectionBestFeatures[feat] = weight
            else:
                collectionBestFeatures[feat] += weight

        f, w = features[0]
        if f not in collectionTopFeatures:
            collectionTopFeatures[f] = 1
        else:
            collectionTopFeatures[f] += 1

    listBestFeatures=sorted(collectionBestFeatures.items(),key=operator.itemgetter(1),reverse=True)
    listTopFeatures=sorted(collectionTopFeatures.items(),key=operator.itemgetter(1),reverse=True)
    return listBestFeatures,listTopFeatures

def reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown=[],label_unk=[],reg=0):
    if reg:
        feature_importance, predict_dict=RFU.rand_for(X_train, X_test, y_train, y_test,x_unknown)
        RFU.plot_importance(feature_importance, X_test,y_test,predict_dict,x_unknown)
        print('predictions from RandomForest Regression')
        RFU.print_predict(y_test,predict_dict,label_test,label_unk=label_unk)
        num_feat=3
        variables=feature_importance.index[0:num_feat]
        #print('\nGLM using variables from RF regression')
        #RFU.run_glm(X_train,y_train,X_test,y_test,variables,'RFreg',label_test)
        #lin_reg(X_train, X_test, y_train, y_test,variables,label_train,label_test)
    if reg==0 or reg == 2:
        print('\nRANDOM FOREST CLASSIFIER')
        epochs=100
        listBestFeatures,listTopFeatures=start_clusterAnal(X_train, X_test, y_train, y_test,epochs,label_test,x_unknown,label_unk)
        RFU.plot_features(listBestFeatures,str(epochs),'Total Weight ')
        RFU.plot_features(listTopFeatures,str(epochs),'Count ')
        print('best features=',listBestFeatures)
    if reg:
        return feature_importance

if __name__ == '__main__':
    ### arg parsers: -train list, -test list, ycol, train par, drop par, reg
    ### file_dict = {'train': par.train,'test':par.test}
    reg=1 #reg=0 means cluster anal alone, reg=2 means both reg and cluster
    mol='CK_PKA_Gi'
    file_dict={'train':['./resultsCKhalf2_'+mol+'.csv','./resultsCKhalf2_cof_act.csv'], 'test': []}#['resultsCKhalf2_multispine_tag_'+mol+'.csv','./resultsCKhalf2_multispine_tag_cof_act.csv']} #{'train':['results2025oct/ctrl_*.csv'],'test': ['results2025oct/KO*.csv', 'results2025oct/PDE4*.csv']} #
    train_par='' #'-ctrl'#used if test files are not separate or to train on controls
    drop=['DropTime']#,'DecrDur','IncrDur'] 
    ycol='outcomeLTP'
    drop_kin_spine=False
    drop_kin_below=False
    regions=['dend','sa1']
    extra_plots=False
    ### end of parameters
    
    df_dict=RFU.read_files(file_dict,drop)
    if extra_plots:
        pairs=[[ 'AUCabove_dend'+mol,'peak_dend'+mol],['peak_dend'+mol,'AUCabove_sa1cof_act'],['AUCabove_dend'+mol,'IncrDur_dendcof_act']]
        fig1=RFU.paired_feature_plot(pairs,df_dict['train'],ycol)
        if len(df_dict['test']):
            fig2=RFU.paired_feature_plot(pairs,df_dict['test'],ycol)
    ###### Drop_col: columns need to be dropped, because analysis uses all columns, cannot specify only a subset
    drop_col=['Trial']
    if len(df_dict['test']):
        if not re.match('^[0-9\.]*$',df_dict['test']['Trial'][0]):
            df_dict['test']['Par']=df_dict['test']['Par']+df_dict['test']['Trial'] #update par with spine ID
    if drop_kin_spine:
        drop_col=drop_col+['sa1'+mol]
    if drop_kin_below:
        drop_col=drop_col+[col+'_'+reg+mol for col in ['AUCbelow'] for reg in regions] #these are already dropped: 'DropTime','DecrDur',
    newdf={}
    if len(df_dict['test']):
        for k,df in df_dict.items():
            newdf[k]=df.drop([i for i in df.columns for dc in drop_col if dc in i ], axis=1) #not inplace since making assignment
    elif train_par: #extract test df as those parameters beginning with train_par string
        df_dict['train'].drop([i for i in df_dict['train'].columns for dc in drop_col if dc in i ], axis=1, inplace=True)
        params=np.unique(df_dict['train']['Par'])
        train_params=[x for x in params if x.startswith(train_par)]
        test_params=[x for x in params if not x.startswith(train_par)]
        newdf['test']=df_dict['train'].loc[df_dict['train']['Par'].isin(test_params)]      
        newdf['train']=df_dict['train'].loc[df_dict['train']['Par'].isin(train_params)]
    else: #train on random subset of all trials/parameters
        newdf['train']=df_dict['train'].drop([i for i in df_dict['train'].columns for dc in drop_col if dc in i ], axis=1)#not inplace since making assignment
        newdf['test']=[]
    newdf['train'].sort_index(axis=1,inplace=True)    
    if len(newdf['test']): #train on training set, test on testing set
        newdf['test'].sort_index(axis=1,inplace=True)    
        if extra_plots:
            kin_features=[ 'AUCabove_dend'+mol,'peak_dend'+mol]
            feature_mol='cof_act'
            features=['AUC'+where+'_' + struct+feature_mol for where in ['below','above'] for struct in ['dend','sa1']]+['peak_'+struct+feature_mol for struct in ['dend','sa1']]+kin_features
            panels=['1tr','4tr']
            RFU.plot_outcome_feature(features,panels,df_dict['train'],train_par,ycol)
        print('\n***************** train on Ctrl, test on others **************')
        X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk=RFU.select_test_train(newdf['train'],ycol,newdf['test'],label='Par') #separate train and test
        feature_importance=reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk,reg=reg) #,reg=2 for  regression and cluster, reg=0 for cluster only
        entire_df=pd.concat([newdf['train'],newdf['test']],ignore_index=True)
    else:
        entire_df=newdf['train']                            
    print('\n***************** randomly select trials from ctrl and others for both train and test **************')
    X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk=RFU.select_test_train(entire_df,ycol,label='Par') #random select train-test
    feature_importance=reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk,reg=reg) #make reg=1 to do regressions
    #barfig=RFU.importance_bar(feature_importance,4)
    #7. make rand forest regression a class?
    '''CKhalf2: CK_PKA_Gi - 100% correct, without using cof_act.  This is the most similar to prior research, so that is good for consistency
            CK_PKA_PAK: using RF reg, gets 3 wrong, cof_act is 3d important, repeatable
                errors: PDE4enh-4trspaced
            kinase: using RF reg, gets 2 wrong. can get 100% using RF clustering.  cof_act sa1 AUC above is 4th, repeatable

    NEXT:
        two RFs.  train on 2/3 test on 1/3.  then train on 100% and test on long dend.  Alternate: train on 2/3 test on long dend
    '''
