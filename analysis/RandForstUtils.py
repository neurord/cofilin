import numpy as np
import pandas as pd  
import glob
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
plt.ion()
 
def plot_features(list_features,epochs,ylabel=''):
    objects=[name for name,weight in list_features]
    y_pos = np.arange(len(list_features))
    performance = [weight for name, weight in list_features]
    f = plt.figure(figsize=(6,4))

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xticks(rotation=90)
    plt.ylabel(ylabel)
    plt.xlabel('Feature')
    plt.title(ylabel+' over '+epochs+' epochs')
    plt.tight_layout()

def plot_importance(feature_importance, X_test,y_test,pred_dict,x_unk=[]):
    axes = feature_importance.plot.barh()
    axes.legend_.set_visible(False)
    f = plt.gcf()
    f.set_size_inches((6,6))
    axes.set_xlim([0,feature_importance.max()[0]])
    plt.title('Feature Importance - RF reg')
    plt.tight_layout()
    #
    num_plots=0 #these plots are not very informative
    if num_plots>0:
        feats=[feature_importance.index[i] for i in range(num_plots)]
        plt.figure()
        plt.title('Prediction')
        for ft in feats: #e.g. auc above or below for one of the molecules
            plt.scatter(X_test[ft], y_test,alpha=.4,label='actual '+ft)
            plt.scatter(X_test[ft], pred_dict['test'],alpha=.4,label='predict '+ft)
            if len(x_unk):
                plt.scatter(x_unk[ft], pred_dict['unknown'],alpha=.4,label='pred_unk '+ft)
            plt.legend()
            plt.ylabel('outcome')
            plt.xlabel('AUC features')

def importance_bar(feat_import,num_feat):
    fig=plt.figure()
    plt.bar(feat_import.index[0:num_feat],feat_import.RandForReg_FeatImport[0:num_feat])
    plt.ylabel('Feature Importance')
    plt.tick_params(axis='x', labelrotation=45)
    return fig

def plotPredictions(max_feat, train_test, predict_dict, feature_order,epoch,accuracy=''):
    ########## Graph the output using contour graph
    #inputdf contains the value of a subset of features used for classifier, i.e., two different columns from df
    feature_cols = [feat[0] for feat in feature_order]
    
    edgecolors=['k','none']
    '''feature_axes=[(i,i+1) for i in range(0,max_feat,2)]
    #print(feature_axes)
    for cols in feature_axes:
        plt.figure()
        plt.title('Epoch '+str(epoch)+', accuracy='+str(accuracy))
        for key,col in zip(train_test.keys(),edgecolors):
            predict=predict_dict[key]
            df=train_test[key][0]
            plt.scatter(df[feature_cols[cols[0]]], df[feature_cols[cols[1]]],c=predict,cmap=ListedColormap(['b', 'r']), edgecolor=col, s=30,label=key,linewidth=1.5)
            plt.xlabel(feature_cols[cols[0]])
            plt.ylabel(feature_cols[cols[1]])
            plt.legend(title='red: LTP, blue: NC')'''

    fig=plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.title('Epoch '+str(epoch)+', accuracy='+str(accuracy))
    for key,col in zip(train_test.keys(),edgecolors):
        predict=predict_dict[key]
        df=train_test[key][0]
        ax.scatter(df[feature_cols[0]], df[feature_cols[1]], df[feature_cols[2]],c=predict,cmap=ListedColormap(['b', 'r']), edgecolor=col, s=30,label=key,linewidth=1.5)
    ax.set_xlabel(feature_cols[0])
    ax.set_ylabel(feature_cols[1])
    ax.set_zlabel(feature_cols[2])
    ax.legend(title='red: LTP, blue: NC')

def plot_outcome_feature(features,panels,df,train_par,outcome):
    params=np.unique(df['Par'])
    for var in features:
        fig,axes=plt.subplots(len(panels),1,sharex=True)
        for ax,protocol in enumerate(panels):
            prot=[x for x in params if protocol in x and train_par in x]
            for p in prot:
                rows=df.loc[df['Par'].isin([p])]
                axes[ax].scatter(rows[var],rows[outcome],label=p)
            axes[ax].legend()
            axes[ax].set_ylabel(outcome)
        axes[-1].set_xlabel(var)
    
def paired_feature_plot(pairs,df,ycol):
    fig,axes=plt.subplots(len(pairs),1)
    colors=['r','b']
    labels=['NC','LTP']
    plot_df=df[df[ycol].notnull()] 
    for ax,pair in zip(axes,pairs):
        for outcome in np.unique(plot_df[ycol]):
            rows=plot_df.loc[plot_df[ycol]==outcome]
            ax.scatter(rows[pair[0]],rows[pair[1]],color=colors[int(outcome)],label=labels[int(outcome)])
        ax.legend()
        ax.set_ylabel(pair[1])
        ax.set_xlabel(pair[0])
    return fig
    
def merge_files(files,drop_col):
    merge_dfs=[]
    suffix=[]
    for f in files:
        merge_dfs.append(pd.read_csv(f))
        suffix.append(merge_dfs[-1].sigmol[0])
        merge_dfs[-1].drop([i for i in merge_dfs[-1].columns for dr in drop_col if dr in i ], axis=1, inplace=True)
        if len(merge_dfs)>1: #this might actually work to sequentially merge more than 2 dfs per pattern
            if len(merge_dfs)==2:
                sufx=[s for s in suffix]
            else:
                sufx=[None,suffix[-1]]
            merge_dfs[0]=merge_dfs[0].merge(merge_dfs[-1],on=['Trial','Par'],suffixes=sufx) 
    return merge_dfs

def read_files(file_dict,drop_col=[]):
    df_dict={key:[] for key in file_dict.keys()}
    for ftype,patterns in file_dict.items():
        if len([x for x in patterns if '*' in x]):
            for pat in patterns:
                files=glob.glob(pat) #should be two files - one for cofact and one for kinases
                merge_dfs=merge_files(files,drop_col)
                if len(files):
                    df_dict[ftype].append(merge_dfs[0])
        elif len(patterns):
            merge_dfs=merge_files(patterns,drop_col)
            df_dict[ftype].append(merge_dfs[0])
        else:
            print('no files for',ftype)
        if len(df_dict[ftype]):
            df_dict[ftype]=pd.concat(df_dict[ftype],ignore_index=True)
            df_dict[ftype].drop([i for i in df_dict[ftype].columns if 'sigmol' in i ], axis=1, inplace=True)
    return df_dict

def select_test_train(df1, ycol,df2=[],label=''):
    import copy
    ##########################################
    from sklearn.model_selection import train_test_split
    label_train=[]
    label_test=[]
    label_unk=[]
    drop_cols=[ycol]
    if len(df2):
        x_unknown= pd.concat([df2[df2[ycol].isnull()],df1[df1[ycol].isnull()]]) #could be some unknowns in training set
        df2= df2[df2[ycol].notnull()] 
        df1= df1[df1[ycol].notnull()] 
        y_train=df1[ycol]
        y_test=df2[ycol]
        X_train=copy.copy(df1)
        X_test=copy.copy(df2)
    else:
        x_unknown= df1[df1[ycol].isnull()]
        df1= df1[df1[ycol].notnull()] 
        #y=y[df1.index]  
        y = df1[ycol] 
        X_train, X_test, y_train, y_test = train_test_split(df1, y, test_size=0.33, random_state=42)
    if label:
        label_train=X_train[label]
        label_test=X_test[label]
        if len(x_unknown):
            label_unk=x_unknown[label]
        drop_cols.append(label)
    X_train.drop(drop_cols, axis=1,inplace=True)
    X_test.drop(drop_cols, axis=1,inplace=True)
    if len(x_unknown):
        x_unknown.drop(drop_cols, axis=1,inplace=True)
    return X_train, X_test, y_train, y_test, label_train,label_test,x_unknown,label_unk

def  conf_matrix_plot(conf_matrix,title=None):
    from sklearn.metrics import ConfusionMatrixDisplay
    fig,ax=plt.subplots(1,2,figsize=(10,6))
    ConfusionMatrixDisplay(confusion_matrix=conf_matrix['train']).plot(ax=ax[0])
    ConfusionMatrixDisplay(confusion_matrix=conf_matrix['test']).plot(ax=ax[1])
    fig.suptitle(title)
    
def rand_for(X_train, X_test, y_train, y_test,x_unknown):    
    from sklearn.ensemble import RandomForestRegressor
    regr = RandomForestRegressor(n_estimators=100)#;
    regr.fit(X_train, y_train)
    X=pd.concat([X_train,X_test])
    #print & plot some results
    print('***************** Random Forest Regression: ','train corr',round(regr.score(X_train,y_train),4),'test corr',round(regr.score(X_test,y_test),4),'*********************')
    feat_import_df = pd.DataFrame(regr.feature_importances_,X.columns,columns=['RandForReg_FeatImport']).sort_values('RandForReg_FeatImport',ascending=False)
    train_test = {'train':(X_train,y_train), 'test':(X_test, y_test)}
    predict_dict,conf_matrix,accuracy=score(train_test,regr,x_unknown)
    conf_matrix_plot(conf_matrix,title='Reg')
    max_feat=4
    feature_order=[(feat_import_df.index[i],feat_import_df['RandForReg_FeatImport'].iloc[i]) for i in range(max_feat)]
    print('top features=',feature_order)
    plotPredictions(max_feat, train_test, predict_dict, feature_order,epoch='reg',accuracy=accuracy['test'])
    #return feature_importance_df, y_pred
    res,sortedpval=single_glm(X_train,y_train,[feat[0] for feat in feature_order[0:3]])
    print('   ******** GLM results using top features from Rand For Regr\n') 
    print(res.summary())
    return feat_import_df, predict_dict

def score(train_test,rfmodel,x_unk=[]):
    from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
    #calculate a score, show the confusion matrix
    predict_dict = {};conf_matrix={};accuracy={}
    for nm,(df,labl) in train_test.items():
        predict = rfmodel.predict(df)
        predict_dict[nm] = predict
        conf_matrix[nm]=confusion_matrix(labl,[round(p) for p in predict])
        accuracy[nm] = round(accuracy_score(labl,[round(p) for p in predict]),3)
    if len(x_unk):
        predict_dict['unknown']=rfmodel.predict(x_unk)
    else:
        predict_dict['unknown']=[]
    return predict_dict,conf_matrix,accuracy

import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import datasets, linear_model
from scipy.stats import pearsonr

def print_predict(ytest,pred_dict,ylabels,accuracy=None,incorrect_only=False,label_unk=[]):
    print('par          obs pred delta')
    delta=[]
    for yt,ypsk in zip(ytest,pred_dict['test']):
        yrnd=round(ypsk)
        yrnd=round(ypsk-0.15) #change threshold to 0.65 instead of 0.5
        if yt==1:
            delta.append(0 if ypsk>yt else yt-yrnd)
        elif yt==0:
            delta.append(0 if ypsk<yt else yt-yrnd)
    if incorrect_only:
        for ylbl,yt,ypsk,d in zip(ylabels,ytest,pred_dict['test'],delta):
            if d != 0:
                print(ylbl.rjust(12), yt,' ',round(ypsk,2), ' ',d)
    else:
        for ylbl,yt,ypsk,d in zip(ylabels,ytest,pred_dict['test'],delta):
            print(ylbl.rjust(12), yt,' ',round(ypsk,2), ' ',d)
    print('Mean Delta=',np.mean(delta),'out of',len(ytest),'Test accuracy=',accuracy)
    if len(pred_dict['unknown']):
        print('predictions with unknown outcomes:')
        for ylbl,ypred in zip(label_unk,pred_dict['unknown']):
            print(ylbl.rjust(12), ypred)

def single_glm(Xtrain,ytrain,cols):
    mod = sm.OLS(ytrain,Xtrain[cols]) #Ordinary Least Squares Regression
    res = mod.fit()
    print('   Rsqr adj {}, F pvalue {}'.format (round(res.rsquared_adj,3),res.f_pvalue))
    pvalfeat=[(pval,feat) for feat, pval in zip(cols, res.pvalues)]
    sortedpval=sorted(pvalfeat)
    return res,sortedpval

def run_glm(Xtrain,ytrain,Xtest,ytest,colums,msg,ylabels,xunk=[],lbl_unk=[],sort=True):
    testcols=list(colums.copy())
    final=False
    while not final:
        res,sortedpval=single_glm(Xtrain,ytrain,testcols)
        #select top features from above to use instead of from RFreg:            
        if sortedpval[-1][0]>0.05:
            testcols.remove(sortedpval[-1][1])
            print('   **** not all molecules {} significant, repeating anova with {} ***'.format(list(colums),testcols))      
        else:
            final=True
            print('   **** all molecules significant: {}  ***'.format(testcols))      
    
    print('   ******** GLM results using top features from',msg,'\n') #problem - subsequent features might be correlated with intial ones, or account for residuals
    print(res.summary())
    print('\nNow try linear regression using linear_model.LinearRegression')
    regr = linear_model.LinearRegression(fit_intercept=False);random_state = 1000 #Ordinary Least Squares Regression, using features from RFreg
    # Train the model using the training sets
    regr.fit(Xtrain[testcols], ytrain)
    # Make predictions using the testing set
    predict_dict={}
    predict_dict['test'] = regr.predict(Xtest[testcols])
    if len(xunk):
        predict_dict['unknown']=regr.predict(xunk[testcols])
    else:
        predict_dict['unknown']=[]
    print('   Linear Regression score=',regr.score(Xtrain[testcols], ytrain),'Coefficients: \n')
    print("      Mean squared error on TEST set: %.2f" % mean_squared_error(ytest, predict_dict['test']))
    # Explained variance score: 1 is perfect prediction
    R2_sk,pv_sk=pearsonr(ytest,predict_dict['test'])
    print('      Variance score on TEST set: %.2f; R2, pval= %.3f,%.3f' % (r2_score(ytest, predict_dict['test']),R2_sk,pv_sk ))
    print_predict(ytest,predict_dict,ylabels,label_unk=lbl_unk)
