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

def reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown=[],label_unk=[],regtype=0):
    if regtype:
        feature_importance, predict_dict=RFU.rand_for(X_train, X_test, y_train, y_test,x_unknown)
        RFU.plot_importance(feature_importance, X_test,y_test,predict_dict,x_unknown)
        print('predictions from RandomForest Regression')
        RFU.print_predict(y_test,predict_dict,label_test,label_unk=label_unk)
        num_feat=3
        variables=feature_importance.index[0:num_feat]
        #print('\nGLM using variables from RF regression')
        #RFU.run_glm(X_train,y_train,X_test,y_test,variables,'RFreg',label_test)
        #lin_reg(X_train, X_test, y_train, y_test,variables,label_train,label_test)
    if regtype==0 or regtype == 2:
        print('\nRANDOM FOREST CLASSIFIER')
        epochs=100
        listBestFeatures,listTopFeatures=start_clusterAnal(X_train, X_test, y_train, y_test,epochs,label_test,x_unknown,label_unk)
        RFU.plot_features(listBestFeatures,str(epochs),'Total Weight ')
        RFU.plot_features(listTopFeatures,str(epochs),'Count ')
        print('best features=',listBestFeatures)
    if regtype:
        return feature_importance,predict_dict

if __name__ == '__main__':
    ### arg parsers: -train list, -test list, ycol, train par, drop par, reg
    ### file_dict = {'train': par.train,'test':par.test}
    regtype=1 #regtype=0 means cluster anal alone, regtype=2 means both regtype and cluster
    mol='CK_PKA_PAK'
    thr='_0.05_0.08'
    file_dict={'train':['./resultsCKhalf2'+thr+mol+'.csv','./resultsCKhalf2_0.04_0.11cof_act.csv'], 'test': ['./resultsCKhalf2'+thr+'multispinetag_'+mol+'.csv','./resultsCKhalf2_0.04_0.11multispinetag_cof_act.csv']} #[]}#{'train':['results2025oct/ctrl_*.csv'],'test': ['results2025oct/KO*.csv', 'results2025oct/PDE4*.csv']} #
    train_par='' #'-ctrl'#used if test files are not separate or to train on controls
    drop=['DropTime']
    ycol='outcomeLTP'
    drop_kin_spine=False
    drop_kin_below=False
    regions=['dend','sa1']
    extra_plots=True
    create_output_df=True
    ### end of parameters
    
    df_dict=RFU.read_files(file_dict,drop)
    if extra_plots:
        pairs=[[ 'peak_sa1'+mol,'IncrDur_dend'+mol],['peak_sa1'+mol,'AUCabove_sa1cof_act'],['peak_sa1'+mol,'DecrDur_dendcof_act']]
        fig1=RFU.paired_feature_plot(pairs,df_dict['train'],ycol,'train')
        if len(df_dict['test']):
            fig2=RFU.paired_feature_plot(pairs,df_dict['test'],ycol,fig=fig1,title='train and test')
            #fig2=RFU.paired_feature_plot(pairs,df_dict['test'],ycol,title='test')
    ###### Drop_col: columns need to be dropped, because analysis uses all columns, cannot specify only a subset
    drop_col=['Trial']
    if len(df_dict['test']):
        if not re.match('^[0-9\.]*$',df_dict['test']['Trial'][0]):
            df_dict['test']['Par']=df_dict['test']['Par']+df_dict['test']['Trial'] #update par with spine ID
        else:
            df_dict['test']['Par']=df_dict['test']['Par']+df_dict['test']['Trial'] #keep trial as part of par anyway
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
            kin_features=[ 'peak_sa1'+mol,'AUCabove_sa1cof_act','IncrDur_dend'+mol]
            feature_mol='cof_act'
            features=['AUC'+where+'_' + struct+feature_mol for where in ['below','above'] for struct in ['dend','sa1']]+['peak_'+struct+feature_mol for struct in ['dend','sa1']]+kin_features
            panels=['1tr','4tr']
            RFU.plot_outcome_feature(features,panels,df_dict['train'],train_par,ycol)
        print('\n***************** train on Ctrl, test on others **************')
        X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk=RFU.select_test_train(newdf['train'],ycol,newdf['test'],label='Par') #separate train and test
        feature_importance,predict_dict=reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk,regtype=regtype) #,regtype=2 for  regression and cluster, reg=0 for cluster only
        entire_df=pd.concat([newdf['train'],newdf['test']],ignore_index=True)
    else:
        entire_df=newdf['train']                            
    print('\n***************** randomly select trials from ctrl and others for both train and test **************')
    X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk=RFU.select_test_train(entire_df,ycol,label='Par') #random select train-test
    feature_importance,predict_dict=reg_and_plot(X_train, X_test, y_train, y_test,label_train,label_test,x_unknown,label_unk,regtype=regtype) #make regtype=1 to do regressions

    if create_output_df:
        top_features=feature_importance[0:4].index
        output_df=X_train[top_features].copy() #create new df with top four feature
        output_df.loc[:,'predict']=predict_dict['train']#add in prediction and whether train or test, (c) parameter+trial, 
        output_df.loc[:,'train_test']=['train']*len(predict_dict['train'])
        output_df.loc[:,'ParTrial']=label_train
        output_df.loc[:,'outcomeLTP']=y_train
        y_unk=[2]*len(label_unk)
        for tp,Xdf,labeldf,outcome in zip(['test','unknown'],[X_test,x_unknown],[label_test,label_unk],[y_test,y_unk]):
            test_rows=Xdf[top_features].copy()
            test_rows.loc[:,'predict']=predict_dict[tp]
            test_rows.loc[:,'train_test']=[tp]*len(predict_dict[tp])
            test_rows.loc[:,'ParTrial']=labeldf
            test_rows.loc[:,'outcomeLTP']=outcome
            output_df=pd.concat([output_df,test_rows])
        output_df.sort_index(inplace=False)
        output_df.to_csv(mol+'_predict_df.csv')
        feature_importance.to_csv(mol+'_features.csv')

