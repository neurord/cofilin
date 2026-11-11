import os
import sys
import numpy as np 
from matplotlib import pyplot as plt
plt.ion()
import utils
from normalize import load_data

label_dict={'sa1[0]':'spine','dend':'dend','CK_PKA_PAK':'kinase','CK_PKA_Gi':'kinase','cof_act':'cofilin', 'actCof':'cofilin (nM)','Ractot':'Total RacGTP (nM)', 'sshfree':'SSH (nM)'}

def load_data_time(pars,f,onset_time):
    par = f.split(mol)[0].split('Model_Cof-')[-1].rstrip('-')#this is dangerous !!! change this when file naming changes
    data,headers,time,=load_data(os.path.join(pars.dir, f))
    if onset_time[f] !=0: #put stimulation at t=0
        time=np.arange(-onset_time[f],time[-1]-onset_time[f]+time[1],time[1])
    return data,headers,time,par

def updatey(ax,ymin,ymax):
    newyn,newyx=ax.get_ylim()
    ymin=np.nanmin([newyn,ymin])
    ymax=np.nanmax([newyx,ymax])
    return ymin,ymax

def plot_data(time,traces,colors,split_txt,split_num,thresholds=[]): 
    mols=list(traces.keys()) #one row per signature molecules
    regions=list(traces[mols[0]].keys())#one col per region
    fig,ax=plt.subplots(len(mols),len(regions))
    for i,mol in enumerate(mols):
        (ymin,ymax)=(0,0)
        for j,reg in enumerate(regions):
            maxvals={par:np.max(traces[mol][reg][par]['mean']) for par in traces[mol][reg].keys()}
            maxval_sort={k: v for k, v in sorted(maxvals.items(), reverse=True, key=lambda item: item[1])}
            z_index={k:i*10 for i,k in enumerate(maxval_sort.keys())}
            for par,col in zip(traces[mol][reg].keys(),colors):
                lbl=par.split('-')[split_num].split(split_txt)[-1]
                ax[i,j].plot(time,traces[mol][reg][par]['mean'],label=lbl,color=col,zorder=z_index[par])
            ymin,ymax=updatey(ax[i,j],ymin,ymax)
            ax[i,j].set_xlabel('Time (sec)')
            mlabel=label_dict[mol] if mol in label_dict else mol + '(nM)'
            rlabel=label_dict[reg] if reg in label_dict else reg
            ax[i,j].set_ylabel(mlabel+' '+rlabel)
            ax[i,j].legend(loc='upper right')
        for j,thresh in enumerate(thresholds[mol]):
            ax[i,j].hlines(thresh,time[0],time[-1],color='gray',label='thresh',linestyles='dashed')
        for j in range(len(regions)):
            ax[i,j].set_ylim([ymin,ymax])
    return fig

def plot_10u(time,traces,colors,split_txt,split_num,thresholds=[]): 
    reg_label_dict={'sa1[0]':'spine 0','dend':'dend','sa1[1]':'spine 1','sa1[2]':'spine 2'}
    mols=list(traces.keys()) #one row per signature molecules
    regions=list(traces[mols[0]].keys())#one col per region
    pars=list(traces[mols[0]][regions[0]].keys())
    fig,ax=plt.subplots(len(mols),len(pars))
    for i,mol in enumerate(mols):
        (ymin,ymax)=(0,0)
        for reg,col in zip(regions,colors):
            if len(pars)>1:
                for j, par in enumerate(traces[mol][reg].keys()):
                    lbl=reg_label_dict[reg] if reg in reg_label_dict else reg
                    if len(time)!=len(traces[mol][reg][par]['mean']):
                        time=np.linspace(time[0],time[-1],len(traces[mol][reg][par]['mean']))
                    ax[i,j].plot(time,traces[mol][reg][par]['mean'],label=lbl,color=col)
                    ymin,ymax=updatey(ax[i,j],ymin,ymax)
                    ax[i,j].set_xlabel('Time (sec)')
                    mlabel=label_dict[mol] if mol in label_dict else mol + ' (nM)'
                    ax[i,j].set_ylabel(mlabel)
                    ax[i,j].legend(loc='upper right')
            else:
                par=pars[0]
                lbl=reg_label_dict[reg] if reg in reg_label_dict else reg
                if len(time)!=len(traces[mol][reg][par]['mean']):
                    time=np.linspace(time[0],time[-1],len(traces[mol][reg][par]['mean']))
                ax[i].plot(time,traces[mol][reg][par]['mean'],label=lbl,color=col)
                ax[i].set_xlabel('Time (sec)')
                mlabel=label_dict[mol] if mol in label_dict else mol  + ' (nM)'
                ax[i].set_ylabel(mlabel)
                ax[i].legend(loc='upper right')
        if len(thresholds) and len(pars)<=1:
            for j in range(len(pars)):
                ax[i].hlines(thresholds[mol][0],time[0],time[-1],color='gray',label='thresh',linestyles='dashed')
        if len(pars)>1:
            for j,par in enumerate(pars):
                ax[i,j].set_ylim([ymin,ymax])
                ax[0,j].set_title(par.split('-')[-1].split(split_txt)[split_num].strip('_').capitalize()[0:-3],fontweight="bold") #for tagging: [0:-3]
                ax[i,j].hlines(thresholds[mol][0],time[0],time[-1],color='gray',label='thresh',linestyles='dashed')
    return fig

def plot_columns(time,cols,traces,colors,split_txt,thresholds=[],exclude=[],bar_data=None): 
    mols=list(traces[cols[0]].keys()) #one row per signature molecules
    regions=list(traces[cols[0]][mols[0]].keys())#one col per region
    if bar_data:
        num_rows=len(mols)*len(regions)-len(exclude)+1
    else:
        num_rows=len(mols)*len(regions)-len(exclude)
    fig,ax=plt.subplots(num_rows,len(cols))
    for ii, ckey in enumerate(cols):
        axnum=0
        for i,mol in enumerate(mols):
            for j,reg in enumerate(regions):
                if not mol+reg in exclude:
                    for par,col in zip(traces[ckey][mol][reg].keys(),colors):
                        ax[axnum,ii].plot(time,traces[ckey][mol][reg][par]['mean'],label=par.split('-')[0].split(split_txt)[-1],color=col) 
                        #print('label',par,par.split('-'))
                    ax[axnum,ii].set_xlabel('Time (sec)')
                    mlabel=label_dict[mol] if mol in label_dict else mol  + ' (nM)'
                    rlabel=label_dict[reg] if reg in label_dict else reg
                    ax[axnum,ii].set_ylabel(mlabel+' '+rlabel)
                    if axnum==2:
                        ax[axnum,ii].legend(loc='best')
                    else:
                        ax[axnum,ii].legend(loc='upper right')
                    axnum+=1 
        ax[0,ii].set_title(ckey.strip('_').capitalize(),fontweight="bold")
    barnum=axnum
    axnum=0
    for i,mol in enumerate(mols):
        for j,reg in enumerate(regions):
            if not mol+reg in exclude:
                (ymin,ymax)=(0,0)
                for ii, ckey in enumerate(cols):
                    ymin,ymax=updatey(ax[axnum,ii],ymin,ymax)
                    ax[axnum,ii].hlines(thresholds[mol][j],time[0],time[-1],color='gray',label='thresh',linestyles='dashed')
                for ii, ckey in enumerate(cols):
                    if np.round(ymax,1)<ymax:
                        ymax=np.round(ymax,1)+0.1
                    ax[axnum,ii].set_ylim([np.round(ymin,1),ymax])
                axnum+=1
    if bar_data:
        bar_panel(fig,ax,bar_data,barnum)
    return fig

def bar_panel(fig,ax,bar_data,row):
    import pandas as pd
    df=pd.read_csv(bar_data, sep=",")
    for i,mol in enumerate(['pLIMK_LIMK','pCof_Cof']):
        ax[row,i].bar(df.condition,df[mol+'_ratio'],color='grey')
        ax[row,i].errorbar(df.condition,df[mol+'_ratio'],yerr=df[mol+'_se'],fmt='o',color='k',capsize=3)
        ax[row,i].set_ylabel(mol.replace('_','/'))
        #ax[row,i].set_xlabel('condition')
    return fig

def tweak_fig(fig,yrange=None,xrange=None,axnum=None): 
    ax=fig.axes
    if isinstance(axnum,int):
        axes=ax[0:axnum]
    elif isinstance(axnum,list):
        axes=[ax[a] for a in axnum]
    else:
        axes=ax
    for axis in axes:
        if yrange:
            axis.set_ylim(yrange)
        if xrange:
            axis.set_xlim(xrange)
    #fig.tight_layout()

def add_labels(fig,labels=None):#FIXME: specify x,y coords for each label
    axes=fig.axes
    if not labels:
        import string
        labels=list(string.ascii_uppercase)[0:len(axes)]
    for ax,lbl in zip(axes,labels):
        ax.text(-0.15, 1.1, lbl, transform=ax.transAxes,
            fontweight='bold', va='top', ha='right',fontsize=14)

def region_columns(reg_cols,headers,reg,f):
    for coltype in reg_cols.keys(): 
        print('extracting columns for reg=',reg,'for file',f,'coltype',coltype)
        if coltype=='mean':
            reg_cols[coltype] = [i for i, h in enumerate(headers) if reg in h and 'std' not in h.lower() and 'sub' not in h.lower() and 'cyt' not in h.lower()]
        else:  
            reg_cols[coltype]= [i for i, h in enumerate(headers) if reg in h and coltype in h.lower() and 'sub' not in h.lower() and 'cyt' not in h.lower()] 
    return reg_cols

if __name__ == '__main__':
    ARGS="cof_act CK_PKA_PAK -keys 4tr ctrl sig.txt -dir resultsCKhalf2 -reg dend sa1[0] -thresh 0 0 -remove 10u basal" # 4 train figure 5
    #ARGS="cof_act CK_PKA_PAK -keys 1tr ctrl sig.txt -dir resultsCKhalf2 -reg dend sa1[0] -thresh 0 0" #1 train figure 4
    #ARGS="cof_act CK_PKA_PAK -keys 4tr sig.txt -col_key spaced massed -dir resultsCKhalf2 -reg dend sa1[0] -thresh 0.22 -1 1 .1 -color KO -remove 10u PDE4 basal" #massed vs spaced, ctrl and KO
    #ARGS="RacPAKLIMK PKAcLIMK pLIMK  -keys 4tr avg.txt spaced -dir resultsCKhalf2 -reg dend sa1[0] -color mol -remove PDE4 basal 10u -thresh -10 -10 -10" #molecules, PDE4 and spaced only
    #ARGS="CKtot PKAphos dualCK_PKA  -keys 4tr avg.txt spaced -dir resultsCKhalf2 -reg dend sa1[0] -color mol -remove KO basal 10u Kal -thresh -10 -10 -10" #molecules, PDE4 and spaced only
    #ARGS="dualPKA_PAK EpacAMP Gibg  -keys 4tr avg.txt spaced -dir resultsCKhalf2 -reg dend sa1[0] -color mol -remove KO basal 10u -thresh -10 -10 -10" #molecules figure, PDE4 and spaced only
    #ARGS="KalCKtot KalPKAc pKal -keys 4tr avg.txt spaced -dir resultsCKhalf2 -reg dend sa1[0] -color mol -remove basal KO 10u -thresh -10 -10 -10" #molecules figure, PDE4 and spaced only
    #ARGS="RacPAKLIMK PKAcLIMK pLIMK -keys 4tr avg.txt -dir resultsCKhalf2 -reg dend sa1[0] -color mol -col_key spaced massed -remove basal PDE4 10u -thresh -10 -10 -10 -10 -10 -10 " #molecules figure, KO and spaced only
    #ARGS="sshfree SSHpLIMK SSHpCof -keys 4tr avg.txt -dir resultsCKhalf2 -reg dend sa1[0] -color mol -col_key spaced massed -remove basal PDE4 10u -thresh -10 -10 -10 -10 -10 -10 " #molecules figure, KO and spaced only
    #ARGS="KalCKtot KalPKAc pKal -keys 4tr avg.txt -dir resultsCKhalf2 -reg dend sa1[0] -color mol -col_key spaced massed -remove basal PDE4 10u -thresh -10 -10 -10 -10 -10 -10 " #molecules figure, KO and spaced only
    #ARGS="pKal pLIMK -keys 4tr avg.txt spaced -dir resultsCKhalf2 -reg dend sa1[0] -color mol -remove basal 10u -thresh 0 0 0 0 0 0 0 0" #molecules figure, both PDE and KO variants, spaced only
    ARGS="cof_act CK_PKA_PAK pLIMK -keys 4tr -col_key massed spaced -dir resultsCKhalf2 -reg dend sa1[0] -thresh 0.22 -1 1 .1 -10 -10 -color PDE4 -remove 10u KO basal trials -bar HavekesBarData.csv" #PDE4 fig 6, with constraints
    #ARGS="Ractot cof_act pLIMK sshfree -keys 4tr 10u -dir resultsCKhalf2 -reg sa1[0] sa1[1] sa1[2] -thresh -100 -100 -100 -100 -color PDE4 -remove basal " #Spatial Specificity Figure 7
    #ARGS="pLIMK RacPAK pKal -keys 4tr 10u -dir resultsCKhalf2 -reg sa1[0] sa1[1] sa1[2] -thresh -100 -100 -100 -color PDE4 -remove basal " #Spatial Specificiy molecules figure
    #ARGS="CK_PKA_PAK cof_act -keys 4trains 10um tag sig.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] -thresh -100 -100 -color PDE4 -remove basal Ip35" #Tagging figure 8
    #ARGS="sshfree SSHpLIMK Ractot pLIMK -keys 10u 4trains tag avg.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] -color PDE4 -remove basal spaced -thresh -100  -100 " #CaNCamCa4pSSH #Tagging molecules figure 9
    #ARGS="CaNCamCa4 RacPAK -keys 10u 4trains tag avg.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] dend -color PDE4 -remove basal spaced -thresh -100  -100 " #Spatial Specificiy molecules figure
    #ARGS="Ractot PKAphos Ip35PP1 sshfree -keys 4trains 10um tag avg.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] -thresh 0.22 0.1 -color PDE4 -remove basal" #Tagging molecules figure 
    #ARGS="pLIMK pCof sshfree SSHpLIMK -keys 4trains 10um tag avg.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] dend -thresh 550 500 8950 26 -color PDE4 -remove basal spaced" #Tagging molecules figure
    #ARGS="Ca CamCa4 CaNCamCa4 CalbinC -keys 4trains 10um tag avg.txt -dir Exp10umtag -reg sa1[0] sa1[1] sa1[2] dend -thresh 550 500 8950 26 -color PDE4 -remove basal spaced" #Tagging molecules figure
    #ARGS='CK_PKA_PAK -keys predict_df' #Random Forest Figure 10
    exclude=['CK_PKA_PAKsa1[0]', 'cof_actdend','pLIMKsa1[0]'] #FIXME: args? not used for long dend plots  []#

    reg_cols={'mean':[],'std':[]}
    colors={'1tr':['#7BC8F6','#0000FF','gray','#FA8072','#8C000F'],'4tr':['red','black'],'KO':['black','blue','red'],'PDE4':['black','red','blue','grey'],'mol':['black','blue','#8C000F','#FA8072','#7BC8F6']}
    #possibly use 4 colors from Seismic color map - 70,120,170,220
    try:
        args = ARGS.split()
        print("ARGS =", ARGS, "commandline=", args)
        do_exit = False 
    except NameError: #NameError refers to an undefined variable (in this case ARGS)
        args = sys.argv[1:]
        import os
        mydir=os.getcwd()
        sys.path.append(mydir)
        print("commandline =", args)
        do_exit = True
    pars=utils.parse_args(args,do_exit)
    #exclude=[m+'dend' for m in pars.mols]
    if pars.color:
        use_colors=colors[pars.color]
        split_txt=pars.color
        split_num=0 #take 1st part after split par on '-', then split on split_txt
        if '10u' in pars.keys:
            split_txt='4tr'
            split_num=-1
        elif 'tag' in pars.keys:
            split_txt='4trains'
            split_num=-1
    elif 'predict_df' not in pars.keys:
        use_colors=colors[pars.keys[0]]
        split_txt='tr'
        split_num=1 #take 2nd part after split par on '-', then split on split_txt

    if len(pars.thresh)==len(pars.reg)*len(pars.mols):
        thresh={mol:[float(pars.thresh[j]) for j in range(i*len(pars.reg),(i+1)*len(pars.reg))] for i,mol in enumerate(pars.mols)}
    elif len(pars.thresh)==len(pars.mols):
        thresh={mol:[float(pars.thresh[i]) for j in range(i*len(pars.reg),(i+1)*len(pars.reg))] for i,mol in enumerate(pars.mols)}
    else:
        thresh=[]

    if 'predict_df' in pars.keys:
        import pandas as pd
        import RandForstUtils as RFU
        mol=pars.mols[0]
        plot_df=pd.read_csv(mol+'_'+pars.keys[0]+'.csv',sep=',',index_col='index')
        features=plot_df.columns[0:4]
        feat_df=pd.read_csv(mol+'_features.csv',sep=',')
        pairs=[[ features[0],features[1]],[features[0],features[2]],[features[0],features[3]]]
        ycol='outcomeLTP'
        for ii,tp in enumerate(np.unique(plot_df['train_test'])):
            rows=plot_df.loc[plot_df['train_test']==tp]
            if ii==0:
                fig,lines,line_labels=RFU.paired_feature_plot(pairs,rows,ycol,title=tp,lines=[],line_labels=[])
            else:
                fig,lines,line_labels=RFU.paired_feature_plot(pairs,rows,ycol,fig=fig,title='train and test',lines=lines,line_labels=line_labels)

    elif pars.col_key is None:
        reg_data={mol:{reg:{} for reg in pars.reg} for mol in pars.mols}

        for mol in pars.mols:
            traces_files = utils.search_files(pars.dir, pars.keys+['-'+mol+'-'])
            if not len(traces_files): #if plotting both sig and non-sig molecules in same graph
                new_pars=[p for p in pars.keys]
                if 'sig.txt' in new_pars:
                    new_pars.remove('sig.txt')
                    new_pars.append('avg.txt')
                traces_files = utils.search_files(pars.dir, new_pars+[mol])
            traces_files=utils.remove_files(traces_files,pars.dir,pars.remove,pars.keys)
            onset_time={f: 300 if '4tr' in f else 500 for f in traces_files}
            for f in traces_files:
                data,headers,time,par=load_data_time(pars,f,onset_time)

                for reg in reg_data[mol]:
                    reg_data[mol][reg][par]={st:[] for st in reg_cols.keys()}
                    reg_cols=region_columns(reg_cols,headers,reg,f)
                    for coltype in reg_cols.keys():
                        if len(reg_cols[coltype]):
                            reg_data[mol][reg][par][coltype] = data[:,reg_cols[coltype]]

        if '10u' in pars.keys or '10um' in pars.keys:
            fig=plot_10u(time,reg_data,use_colors,split_txt,split_num,thresholds=thresh)
        else:
            fig=plot_data(time,reg_data,use_colors,split_txt,split_num,thresholds=thresh)
        axnum=None

    elif pars.col_key:
        #read in both KO and ctrl
        reg_data={col:{mol:{reg:{} for reg in pars.reg} for mol in pars.mols} for col in pars.col_key}

        for ckey in pars.col_key:
            for mol in pars.mols:
                traces_files = utils.search_files(pars.dir, pars.keys+[ckey]+['-'+mol+'-'])
                traces_files=utils.remove_files(traces_files,pars.dir,pars.remove)
                onset_time={f: 300 if '4tr' in f else 500 for f in traces_files}
                for f in traces_files:
                    data,headers,time,par=load_data_time(pars,f,onset_time)

                    for reg in reg_data[ckey][mol]:
                        reg_data[ckey][mol][reg][par]={st:[] for st in reg_cols.keys()}
                        reg_cols=region_columns(reg_cols,headers,reg,f)
                        for coltype in reg_cols.keys():
                            if len(reg_cols[coltype]):
                                reg_data[ckey][mol][reg][par][coltype] = data[:,reg_cols[coltype]]
        if pars.bar:
            bar_data=pars.dir+'/'+pars.bar
            axnum=6
        else:
            bar_data=None
            axnum=None
        fig=plot_columns(time,pars.col_key,reg_data,use_colors,pars.color,thresholds=thresh,exclude=exclude,bar_data=bar_data)
    if 'predict_df' not in pars.keys:
        #axnum=[0,1]
        #tweak_fig(fig,xrange=[-100,800],axnum=axnum)
        #axnum=[2,3]
        tweak_fig(fig,xrange=[-100,1400],axnum=axnum)
        #tweak_fig(fig,xrange=[-300,2000],axnum=axnum)
        labels=['A1','A2','B1','B2','C1','C2','D1','D2']
        #labels=[]
    else:
        labels=[]
    add_labels(fig, labels)

#tweak_fig(fig,yrange=[8500,9300],axnum=[-1,-2]) #sshfree - fig 7
#tweak_fig(fig,yrange=[8500,9300],axnum=[0]) #sshfree- fig 9: 
#NEXT STEPS
#1. specify subset of panels


