import importlib
import sys
import numpy as np
import robustness_functions as rf
import pandas as pd
from matplotlib import pyplot as plt
plt.ion()

def graph(x,y,mol):
    plt.figure()
    if len(np.shape(x))==1:
        plt.scatter(x,y,label='data')
    else:
        plt.plot(x,y,label='data')
    coeffs=np.polyfit(x,y,1) #order = 1, fit straight line
    xline=np.array([np.min(x),np.max(x)])
    yline=coeffs[0]*xline+coeffs[1]
    plt.plot(xline,yline,label='fit',color='gray')
    plt.legend()
    plt.xlabel('test value')
    plt.ylabel('prediction')
    plt.title('Ycol='+mol)

def group(x_lda,y):
    plt.figure()
    plt.scatter(x_lda[:,0],x_lda[:,1],c=y,cmap='magma')

def load_graph(loadings,plot_eigs,mol):
    plt.figure()
    num_eigs=min(plot_eigs,np.shape(loadings)[1])
    width=1/(num_eigs+1)
    for eigvec in range(num_eigs): #how  many columns?
        x=np.arange(len(loadings.index))+eigvec*width
        plt.bar(x,loadings.values[:,eigvec], label=loadings.columns[eigvec],tick_label=loadings.index,width=width)
    plt.legend()
    plt.xticks(np.arange(len(loadings.index))+width*num_eigs/3,loadings.index,rotation=45)
    plt.title('Ycol='+mol)

def analyze(X,y_encoded,n_comp=4):
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    sc = StandardScaler() 
    X_scaled = sc.fit_transform(X) #SCALE X values
    '''for ii in X.index:
        plt.scatter(X.iloc[ii],X_scaled[ii]) #scales features 
    plt.show()'''
    #create training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=11) #splits data into 80% train and 20% test
    lda = LinearDiscriminantAnalysis(n_components=n_comp) #set-up linear discriminat analyzer
    X_train_lda = lda.fit_transform(X_train, y_train) #perform LDA
    X_test_lda=lda.transform(X_test) #unused.  Project X_test onto eigenvectors?
    y_pred = lda.predict(X_test) #Test LDA on test data.  
    explained_variance = lda.explained_variance_ratio_
    loadings = pd.DataFrame(lda.scalings_, index=X.columns, columns=[f'LD{i+1}={round(ev,4)}' for i,ev in zip(range(lda.scalings_.shape[1]),explained_variance)]) 
    return loadings,X_train_lda,y_train,y_test,y_pred

def encode_y(y,bins):
    from sklearn.preprocessing import LabelEncoder
    #encode continuous values (ratio of pCof to pCof orig) into groups of values
    yvals=y.values.reshape(len(y))
    if isinstance(bins,int):
        lbls=range(bins)
    else:
        lbls=range(len(bins)-1)
    y_encoded=pd.cut(yvals,bins,labels=lbls)
    #le = LabelEncoder()
    #y_encoded = le.fit_transform(y) #encodes categorical labels as integers
    return y_encoded

def read_robust(fpars,fresults):
    dfpars=pd.read_csv(fpars+'.csv',index_col=0)
    dfres=pd.read_csv(fresults+'.csv',index_col=0,dtype={'index':int})
    dfs=dfpars.merge(dfres,on=['index'])
    return dfs,dfres.columns

if __name__ == '__main__':
    #ARGS='robust/random_change_file2026-10-08 robust/robust_output pCof_Overall pCof_sa1[0] pLIMK_Overall actCof_Overall actCof_sa1[0] SSH_Overall CKtot_Overall PKA_PAK_Overall actRac_Overall' 
    ARGS='robust/random_change_file2026-10-08 robust/Model_Cof-basalctrl_compare pCof_Overall pCof_sa1[0] actCof_Overall actCof_sa1[0] CKtot_Overall PKA_PAK_Overall' 
    plot_eigs=2

    try:
        args = ARGS.split(" ")
        print("ARGS =", ARGS, "commandline=", args)
    except NameError: #NameError refers to an undefined variable (in this case ARGS)
        args = sys.argv[1:]
        print("commandline =", args)

    #read parameters and data files, create df
    par_file=args[0] #list of random parameter changes
    result_file=args[1] #output values
    output_mol=args[2:] #molecule to analyze 
    df,ycols=read_robust(par_file,result_file) #ycols list all output columns in the results file (including spine and dendrite values)

    #separate into X values and Y values
    if isinstance(output_mol,list):
        Ycol=output_mol
    else:
        Ycol=[output_mol]
    Yvals=df[Ycol]
    Xvals=df.drop([i for i in df.columns for dc in ycols if dc in i ], axis=1) 

    #recode the Yvalues in set of categories
    bins=5#[0.7,0.85,0.95,1.05,1.15,1.3] #number of bins or specify bin edges; must be less than or equal to number of samples;  Use 5 with full set of samples
    n_comp=bins-1 #n_comp must be less than num bins  
    for mol in Ycol:
        ycat=encode_y(Yvals[mol],bins)
        #perform LDA
        loadings,X_train_lda,y_train,y_test,y_pred=analyze(Xvals,ycat,n_comp=n_comp)
        print("\nFeature Loadings per Component for "+mol+":")
        print(loadings.sort_values(by=loadings.columns[0]),'\n\ny,')
        for x,y in zip(y_test,y_pred):
            print(x,y)
        load_graph(loadings,plot_eigs,mol)
        graph(y_test,y_pred,mol)
        #group(x_lda,y)

