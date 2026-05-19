import numpy as np 
from matplotlib import pyplot as plt
plt.ion()
from scipy.signal import butter, filtfilt

class DifferenceCalculator:
    
    def __init__(self, std_multiplier, dt, norm,cutoff,regions,fixed_thresh=None):
        self.std_multiplier = std_multiplier
        self.dt = dt
        self.norm=norm
        self.filt_cutoff=cutoff
        if fixed_thresh:
            self.fixed_thresh=True
            self.thresh_hi=fixed_thresh
        else:
            self.fixed_thresh=False
            self.thresh_hi={key:None for key in std_multiplier}
        self.thresh_lo={key:None for key in self.thresh_hi}
        self.stim_onset_idx={} #key = region, updated with each file
        print('std',self.std_multiplier,'thresh',self.thresh_hi,'fixed',self.fixed_thresh,'onset',self.stim_onset_idx)
    
    def compute_difference(self, single_trace, control_basal_mean):
        
        if len(single_trace) != len(control_basal_mean):
            #print(f": Shape mismatch! Traces length: {len(single_trace)}, Basal length: {len(control_basal_mean)}, interpolating to basal time")
            raise ValueError("Mismatch between single_trace and control_basal_mean shapes.")

        return single_trace - control_basal_mean
    
    def norm1(self,trace): #move baseline to zero
        return trace-np.mean(trace[0:self.baseline_idx])

    def norm2(self,trace): #move baseline to one
        return trace/np.mean(trace[0:self.baseline_idx])

    def find_2nd_drop(self,candidates,ends,starts,drop_point_idx,end_drop_idx):
        max_cand=np.min([len(ends),len(starts),len(candidates)])
        if len(candidates)>1:
            durs=[ends[c]-starts[c] for c in range(1,max_cand)]
            if len(durs)>1:
                idx_2=np.argmax(durs)+1
            else:
                #print('durs',durs)
                idx_2=1
            end_drop_idx.append(ends[idx_2])
            drop_point_idx.append(starts[idx_2])
        return end_drop_idx,drop_point_idx

    def crit_points(self,beyond,noise):
        diff = np.diff(beyond.astype(int))
        starts = beyond[np.where(diff > noise)[0] + 1]
        ends=np.hstack((beyond[np.where(diff >noise)[0]],beyond[-1]))
        if diff[0]<=noise: #add in initial point only if 1st point not included
            starts = np.hstack((beyond[0],starts))
        else:
            ends=ends[1:]
        return starts,ends

    
    def auc_points(self,differences,thresh_hi,thresh_lo,region,prn=True): 
        noise=int(20/self.dt) # 20 msec apart is allowed
        #Find points where trace falls below threshold

        below=np.where(differences[self.stim_onset_idx[region]:] < thresh_lo)[0]+self.stim_onset_idx[region]
        if len(below)>1:
            starts_below,ends_below=self.crit_points(below,noise)
            drop_point_idx=[starts_below[0]] #if duration below is below noise, eliminate?
            end_drop_idx=[ends_below[0]]
            num_drops=len(starts_below)
        else:
            num_drops=0
            drop_point_idx=[np.nan]
            end_drop_idx=[np.nan]

        above=np.where(differences[self.stim_onset_idx[region]:]>thresh_hi)[0]+self.stim_onset_idx[region]
        if len(above)>1: 
            starts_above,ends_above=self.crit_points(above,noise)
            max_pt=np.argmax(differences[starts_above[0]:ends_above[0]])+starts_above[0] 
            rise_point_idx=[starts_above[0]]
            end_above_idx=[ends_above[0]]
            num_peaks=len(starts_above)
        else:
            rise_point_idx=[np.nan]
            end_above_idx=[np.nan]
            max_pt=np.nan
            num_peaks=0

        #NEXT: if two or more above times or below times - trickier
        # Compare starts_above and starts_below to figure out second drop
        if num_drops>1 and num_peaks >=1:
            if starts_below[1]<starts_above[0]: #multiple drops, two or more before 1st peak, FIXME: consider multiple drops after the peak?
                candidates=np.where(ends_below<starts_above[0])[0]
                combine=0 #combine 1st and 2nd drop
            elif starts_below[1]> starts_above[0] and starts_below[0]< starts_above[0]:# 1 dip before, 1 or more after 1st peak
                if num_peaks==1: #1 peak, 2 dips, 1 before and 1 after
                    candidates=ends_below #
                else: #num_peaks>1: #a 2nd peak, 1 dip before, 1 or more after, find dips before 2nd peak, 
                    possible_ends=np.where(starts_above>ends_below[1])[0]
                    if len(possible_ends):
                        st_abv_idx=np.min(possible_ends)
                        candidates=np.where (ends_below<starts_above[st_abv_idx])[0]
                    else:
                        candidates=np.where (ends_below<starts_above[1])[0]
                combine=-1 #could combine 2nd and 3rd drop, but we are only finding 1 dip after the peak
            else: # starts_below[0]>starts_above[0] #all dips after 1st peak
                if num_peaks>1: #multiple peaks. more than one dip between the 1st two peaks?
                    possible_ends=np.where(starts_above>ends_below[0])[0]
                    if len(possible_ends):
                        st_abv_idx=np.min(possible_ends)
                        candidates=np.where (ends_below<starts_above[st_abv_idx])[0]
                    else: #no peaks after the dip: use all ends_below
                        candidates=ends_below #np.where (ends_below<starts_above[1])[0]
                else: #multiple dips, all after the single peak
                    candidates=ends_below
                combine=0 #combine 1st and 2nd drop
            if len(candidates)>1:
                end_drop_idx,drop_point_idx=self.find_2nd_drop(candidates,ends_below,starts_below,drop_point_idx,end_drop_idx)
                #instead of multiple small drops, create one larger drop: 
                if combine>-1: 
                    del end_drop_idx[combine]
                    del drop_point_idx[combine+1]

        #Now, deal with AUC above for two or more peaks,
        if num_peaks>1: 
            if num_drops>=1:  #if 1 or more drops
                #if 1st peak is before the drop, only use multiple peaks before the drop, which can be  combined
                if starts_above[0]<starts_below[0]:
                    candidates=np.where(ends_above<starts_below[0])[0]
                elif len(end_drop_idx)>1: #1st peak is after the drop, and 2nd drop exists, only use peaks prior to 2nd drop
                    candidates=np.where(ends_above < end_drop_idx[1])
                else: #1st peak is after the drop, and no 2nd drop, use all peaks
                    candidates=ends_above
            else:
                candidates=ends_above
            combine=0 #combine 1st and 2nd peaks
            end_above_idx,rise_point_idx=self.find_2nd_drop(candidates,ends_above,starts_above,rise_point_idx,end_above_idx)
            if len(end_above_idx)>1:
                max_pt=np.argmax(differences[rise_point_idx[0]:end_above_idx[1]])+rise_point_idx[0]
                if len(end_above_idx)>combine+1:
                    del end_above_idx[combine]
                    del rise_point_idx[combine+1]
        return rise_point_idx, end_above_idx, drop_point_idx, end_drop_idx, [max_pt]
            
    def calc_auc(self,starts,ends,differences):
        #FIXME: calculate AUC for multiple sets of peaks
        #calculate area under the curve between two different points
        auc=[]
        dur=[]
        for start,end in zip(starts,ends):
            if ~np.isnan(start) and ~np.isnan(end):
                auc.append(np.sum(differences[start:end]) * self.dt/1000) #convert to umole-sec
                dur.append((end-start)*self.dt) #units are sec  #alternative: numbe of points above?  Ned to do this in auc points
            else:
                auc.append(0)
                dur.append(0)
        return np.sum(auc),np.sum(dur) #this is fine if two drops or two aboves are adjacent

    def filter_normalize(self,single_traces, control_basal_mean):
        #filter, normalize traces, then compute difference
        b,a=butter(4,self.filt_cutoff,btype='lowpass',fs=(1./(self.dt*1e-3))) # 4 pole filter
        trace_filt=filtfilt(b,a, single_traces, axis=0)
        basal_filt=filtfilt(b,a, control_basal_mean, axis=0)

        if self.norm=='subtract':
            #normalize by subtracting baseline, for both trace and basal.  Then calculate the difference trace
            norm_trace=self.norm1(trace_filt) 
            norm_basal=self.norm1(basal_filt)
        elif self.norm=='divide':
            #normalize by dividing by baseline, for both trace and basal.  Then calculate the difference trace
            norm_trace=self.norm2(trace_filt)  #move baseline to one
            norm_basal=self.norm2(basal_filt)
        difference = self.compute_difference(norm_trace, norm_basal) #pre-stim should be near zero
        return norm_trace,norm_basal,difference
    
    def find_thresh(self,region,control_basal_std,control_basal_mean):
        if self.norm=='subtract': 
            thresh = self.std_multiplier[region] * np.mean(control_basal_std[0:self.baseline_idx])
        elif self.norm=='divide':
            thresh = self.std_multiplier[region] * np.mean(control_basal_std[0:self.baseline_idx]/ np.mean(control_basal_mean[0:self.baseline_idx]))
        return thresh

    def analyze_traces(self, time, single_traces, control_basal_mean, control_basal_std, region, plot=False,ylbl=''):
        #from scipy.signal import butter, filtfilt
        """Calculate drop point and AUC values."""
        norm_trace,norm_basal,difference=self.filter_normalize(single_traces, control_basal_mean) 
        if not self.fixed_thresh: 
            self.thresh_hi[region]=self.find_thresh(region,control_basal_std,control_basal_mean)
            self.thresh_lo[region]=-self.thresh_hi[region]
        else:
            #self.thresh_lo[region]=-self.find_thresh(region,control_basal_std,control_basal_mean)
            self.thresh_lo[region]=-self.thresh_hi[region]
         # Calculate AUC values
        rise_point_idx, above_end_pt,drop_point_idx,end_drop_idx,max_pt=self.auc_points(difference,self.thresh_hi[region], self.thresh_lo[region],region,prn=plot)
        auc_below, dur_below=self.calc_auc(drop_point_idx,end_drop_idx,difference)
        auc_above, dur_above=self.calc_auc(rise_point_idx,above_end_pt,difference)
        if plot:        
            points={'rise_st':rise_point_idx,'rise_ed':above_end_pt,'drop_st':drop_point_idx,'drop_ed':end_drop_idx,'peak_pk':max_pt}
            self.plot_diff(time,[norm_trace,norm_basal,difference],['trace','basal','diff'],[self.thresh_hi[region],self.thresh_lo[region]],points,ylabel=ylbl)
        if np.isnan(max_pt[0]):
            peak=0#np.nan
        else:
            peak=difference[max_pt[0]]
        return auc_above, auc_below, dur_above,dur_below,drop_point_idx[0]*self.dt, peak
    
    def plot_diff(self,time,traces,labels,thresholds=[],points=[],ylabel=''):
        from matplotlib import pyplot as plt
        plt.ion()
        plt.figure()
        markers={'rise':'o','drop':'s','peak':'*'}
        colors={'st':'r','ed':'purple','pk':'k'}
        for trace,label in zip(traces,labels):
            plt.plot(time,trace,label=label)
            plt.xlabel('Time (sec)')
            plt.ylabel(ylabel)
        for thresh in thresholds:
            plt.hlines(thresh,time[0],time[-1],color='gray',label='thresh')
        for key,pts in points.items():
            for p in pts:
                if ~np.isnan(p):
                    col=colors[key.split('_')[1]]
                    mark=markers[key.split('_')[0]]
                    plt.scatter(time[p],trace[p],marker=mark,color=col,s=50,zorder=len(traces)+len(thresholds))
        plt.legend()
        plt.show()
       
    def find_points(self,time,stim_onset_idx,baseline_idx, mean_trace,basal_data,region,ylbl=None):
        #calculate thresholds from basal and critical points from mean_trace
        basal_mean=basal_data[region]['mean']
        basal_std=basal_data[region]['std']
        self.stim_onset_idx[region]=stim_onset_idx
        self.baseline_idx=baseline_idx
        #normalize
        norm_trace,norm_basal,difference=self.filter_normalize(mean_trace, basal_mean) #mean_trace is already region specific
        #calculate thresholds - hi thresh can either be fixed or calculated from basal and std.  Currently, low thresh is calculated
        if not self.fixed_thresh:
            self.thresh_hi[region]=self.find_thresh(region,basal_std,basal_mean)
            self.thresh_lo[region]=-self.thresh_hi[region]
        else:
            #self.thresh_lo[region]=-self.find_thresh(region,basal_std,basal_mean)
            self.thresh_lo[region]=-self.thresh_hi[region]
        # find threshold points
        self.rise_point_idx[region], above_end,self.drop_point_idx[region],self.end_point_idx[region], peakpt =self.auc_points(difference,self.thresh_hi[region], self.thresh_lo[region], region)
        if ylbl:
            points={'rise_st':self.rise_point_idx[region],'rise_ed':above_end,'drop_st':self.drop_point_idx[region],'drop_ed':self.end_point_idx[region],'peak_pk':peakpt}
            self.plot_diff(time,[norm_trace,norm_basal,difference],['trace','basal','diff'],[self.thresh_hi[region],self.thresh_lo[region]],
                       points,ylabel=ylbl+'_mean_'+region)
        return 
    
