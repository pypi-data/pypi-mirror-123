import numpy as np
import pandas as pd

import array

import spacetime_tree_cython
from spacetime_tree_cython import SpaceTimeTree 
    
def get_tree_lag(df,omegacrit,nu,timeweightfn,spaceweightfn,tscale,sscale):
    '''
    get_tree_lag
    
    Driver function for computing tree-lagged features
    
    Arguments:
    
    df: dataframe containing one feature to be lagged
    
    thetacrit: opening solid angle used to decide whether to open nodes - large values cause more
    aggressive aggregation of nodes
    
    nu: arbitrary weight to apply to time coordinate - has dimensions of velocity, but actual
    value depends on units used in dataframe, e.g. if loa is pgm, nu=1 is equivalent to 
    about 50 km/month
    
    timeweightfn: integer value setting choice of how information from earlier timesteps is
    weighted. Allowed choices are
    
              1: exponential weighting, so that data from deltat in the past is weighted by
                 exp(-deltat/tscale)
                 
    spaceweightfn: integer value setting choice of how information from different spatial
    location is weighted. Allowed choices are
              
              1: power law with slope -1, so that data from deltar away in space is weighted
              by (deltar/rscale)^-1
              
              2: power law with slope -2, so that data from deltar away in space is weighted
              by (deltar/rscale)^-2
              
    tscale: float value used to scale times in weighting functions (defaults to 1.0)
    
    rscale: float value used to scale distances in weighting functions (defaults to 1.0)
    
    '''
    
    df=df.fillna(0.0)
    if not(df.index.is_monotonic):
        df=df.sort_index()
        
    pgids,times,power,ncells,pgid_to_longlat,longlat_to_pgid,pgid_to_index,time_to_index,index_to_time=map_pgids_and_times(df)

    pgids=array.array('i',pgids)
    times=array.array('i',times)

    tree=spt_cython.SpaceTimeTree(ncells,power,pgids,times,pgid_to_longlat,longlat_to_pgid,pgid_to_index,time_to_index,index_to_time)
    
    map_pgids_and_times(df)
    
    tree.build_tree(df)
    
    df_treelags=tree.walk(df,thetacrit,nu,timeweightfn,spaceweightfn,tscale,sscale)
    
    return df_treelags
   
def map_pgids_and_times(df):
    '''
	map_pgids_and_times
	   
	This function builds a 2D map in longitude-latitude from the pgids contained in 
	the input dataframe, and creates dicts allowing quick transformation from (long,lat)
	to pgid and vice versa.
	    
	A 1D map of the timesteps in the input df is also built and dicts for mapping 
	timesteps to indices and vice versa are built.
	    
	The largest of the 3 dimensions (longitude extent, latitude extent, time
	interval) is then determined and the smallest power of 2 greater than this 
	value computed.
	   
	The events (long., lat., time) are then embedded and centred in a cubic grid with
	this dimension. 
	'''
	
    PG_STRIDE=720
	
	# get unique pgids
	
    pgids=np.array(list({idx[1] for idx in df.index.values}))
    pgids=np.sort(pgids)
        	
	# convert pgids to longitudes and latitudes
	
    longitudes=pgids%PG_STRIDE
    latitudes=pgids//PG_STRIDE
	
    latmin=np.min(latitudes)
    latmax=np.max(latitudes)
    longmin=np.min(longitudes)
    longmax=np.max(longitudes)

    latrange=latmax-latmin
    longrange=longmax-longmin

	# shift to a set of indices that starts at [0,0]

    latitudes-=latmin
    longitudes-=longmin
        
    # find smallest possible square grid with side 2^ncells which will fit the pgids
        
    latmin=np.min(latitudes)
    latmax=np.max(latitudes)
    longmin=np.min(longitudes)
    longmax=np.max(longitudes)
       
    maxsize=np.max((longrange,latrange))
        
    times=np.array(list({idx[0] for idx in df.index.values}))
    times=np.sort(times)
    
    maxsize=np.max((maxsize,len(times)))    
        
    power=1+int(np.log2(maxsize))

    ncells=2**power
        
    # centre the pgids

    inudgelong=int((ncells-longmax)/2)
    inudgelat=int((ncells-latmax)/2)

    longitudes+=inudgelong
    latitudes+=inudgelat
        
    # centre the times
        
    meantime=int((np.max(times)+np.min(times))/2)
        
    halftime=int(ncells/2)
        
    inudgetime=halftime-meantime
        
    times+=inudgetime

	# make dicts to transform between pgids and (long,lat) coordinate      

    pgid_to_longlat={}
    longlat_to_pgid={}
    pgid_to_index={}

    for i,pgid in enumerate(pgids):
        pgid_to_longlat[pgid]=(longitudes[i],latitudes[i])
        longlat_to_pgid[(longitudes[i],latitudes[i])]=pgid
        pgid_to_index[pgid]=i
            
            
    # make dicts to transform between times and the index of a time in the list
         
    time_to_index={}
    index_to_time={}
          
    for i,time in enumerate(times):
        time_to_index[time]=i
        index_to_time[i]=time
            
    return pgids,times,power,ncells,pgid_to_longlat,longlat_to_pgid,pgid_to_index,time_to_index,index_to_time
    