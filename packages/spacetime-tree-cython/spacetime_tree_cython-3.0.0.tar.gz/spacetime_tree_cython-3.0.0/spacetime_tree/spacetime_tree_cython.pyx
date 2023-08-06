# cython: language_level=3, boundscheck=False, cdivision=True


from cpython cimport array
import array
cimport numpy 
import numpy 

import pandas

cdef class SpaceTimeNode():
    """
    SpaceTimeNode() class
    Defines nodes for insertion in SpaceTimeTree() class
    
    Nodes have:
    
    - nodeid: a unique id
    
    - masterindex, levelindex, level: book-keeping indices giving their tree level and 
      location on that level (not needed once tree has been built)
      
    - parent: parent node
   
    - nleaf: the number of leaf nodes contained within the node's boundaries
 
    - nchild: node's actual number of children
    
    - level: tree level node is a member of
    
    - pgid: if node is a leaf node, the corresponding pg cell id
    
    - time: if node is a leaf node, the corresponding timestep
    
    - isleaf: a flag indicating whether a leaf node
    
    - left, right, bottom, top, past, future: node boundaries
    
    - feature: value of feature held by node
 
    - centre: node's geometric centre
    
    - pgid: the corresponding priogrid cell, if a leaf node (-1 if not a leaf node)
    
    - children: list of node's (up to 8) children
    
    
    """    
     
    cdef public int nodeid
    cdef public int masterindex 
    cdef public int parent
    cdef public int nleaf
    cdef public int nchild
    cdef public int level
    cdef public int pgid
    cdef public int time
    cdef public int isleaf   
    
    cdef public float left
    cdef public float right
    cdef public float bottom
    cdef public float top
    cdef public float past
    cdef public float future
    cdef public float feature
    
    cdef public float[3] centre
    cdef public int[8] children   
    
    def __init__(self,mstr,level,left,right,bottom,top,past,future,centre,isleaf,pgid,time,feature):
    
        self.nodeid = -1
        self.parent = -1
        self.nleaf = 0
        self.nchild = 0
        
        self.masterindex=mstr
        self.level=level
        self.left=left
        self.right=right
        self.top=top
        self.bottom=bottom
        self.past=past
        self.future=future
        self.centre=centre
        self.isleaf=isleaf
        self.pgid=pgid
        self.time=time
        self.feature=feature

        self.children=[-1, -1, -1, -1, -1, -1, -1, -1]

cdef class SpaceTimeTree():
    '''
    SpaceTimeTree() class
    Defines tree class and methods for building, walking and stocking
    
    The class has:
    
    - ncells: size of the cube created to contain the distribution of pg-cells and 
      timesteps in the target dataframe (an integer poer of 2)
      
    - power: the integer power of 2 required to generate ncells
    
    - nleafnodes: total number of leaf nodes in the tree
    
    - pgid_to_longlat: dict for converting pgids to long,lat coords
    
    - longlat_to_pgid: dict reversing the above
    
    - pgid_to_index: dict converting a pgid to location in list of pgids
    
    - time_to_index: dict converting time to index in list of times
    
    - index_to_time: dict reversing the above
    
    - pgids: list of pgids
    
    - times: list of times
    
    - nodes: list of nodes
    
    '''
    
    cdef public int ncells
    cdef public int power
    cdef public int nleafnodes
    
    cdef public dict pgid_to_longlat
    cdef public dict longlat_to_pgid
    cdef public dict pgid_to_index
    cdef public dict time_to_index
    cdef public dict index_to_time
    
    cdef public array.array pgids
    cdef public array.array times
    
    cdef public SpaceTimeNode[:] nodes
    
    def __init__(self,ncells,power,pgids,times,pgid_to_longlat,longlat_to_pgid,pgid_to_index,time_to_index,index_to_time):
        self.ncells=ncells
        self.power=power
        self.pgids=pgids
        self.times=times
        
        self.pgid_to_longlat=pgid_to_longlat
        self.longlat_to_pgid=longlat_to_pgid
        self.pgid_to_index=pgid_to_index
        self.time_to_index=time_to_index
        self.index_to_time=index_to_time

        self.nleafnodes=0
		
    def build_tree(self,df):
    
        '''
	    build_tree
	   
	    This function builds the tree from the leaf nodes downwards.
	   
	    A list with space for all possible nodes is first built and populated with the 
	    leaf nodes actually present in the df the tree was initialised with. 
	   
	    masterindex is a book-keeping device which is a unique location in the list of 
	    all possible nodes.
	   
	    levelindex is retained for debugging purposes - each node has a number indicating
	    its position in its level, constructed in the same way one would number the 
	    squares on a chessboard, stating with a1, b1, c1, etc.
	   
	    Once leaf nodes are populated, work down through the levels, using nodes in the 
	    level above to generate parent nodes in the current level, using masterindex to
	    avoid creating the same parent twice.
	   
	    Once this is done, the list of all possible nodes is compactified to discard 
	    un-needed indices, and all nodeids are reassigned so that the final list of nodes
	    is contiguous.
	   
	    '''

        cdef int cusum
        cdef int p
        cdef int nc
        cdef int pwr
        cdef int nleafnodes
        cdef int itime
        cdef int ipgid
        cdef int time
        cdef int pgid
        cdef int ix
        cdef int iy
        cdef int it
        cdef int ix2
        cdef int iy2
        cdef int iz2
        cdef int levelindex
        cdef int masterindex
        cdef int istart
        cdef int iend
        cdef int ncellsp
        cdef int ncellsp2
        cdef int ncellsp1
        cdef int ncellsp12
        cdef int nodesize
        cdef int inode
        cdef int ichild
        cdef int nnodes
        cdef int ntimes
        cdef int timeoffset
        cdef int imaster
        cdef int iparent
        cdef int inodelevel
        cdef int ispace
        cdef int nleaf
        
        cdef float fix
        cdef float fiy
        cdef float fit
        cdef float mult
        cdef float left
        cdef float right
        cdef float bottom
        cdef float top
        cdef float past
        cdef float future
        cdef float feature
        
        cdef int[:] times = self.times
        cdef int[:] pgids = self.pgids

        
        cdef dict pgid_to_longlat
        cdef dict pgid_to_index
        cdef dict provisional_to_final

        cdef array.array int_array_template = array.array('i', [])
        cdef array.array float_array_template = array.array('f', [])
        
        cdef array.array powers
        cdef array.array cupowers
        
        cdef SpaceTimeNode node
        cdef SpaceTimeNode parent
        cdef SpaceTimeNode[:] nodes

        powers = array.clone(int_array_template, self.power+1, zero=False)
        cupowers = array.clone(int_array_template, self.power+1, zero=False)
        
        cdef int[:] powers_view = powers
        cdef int[:] cupowers_view = cupowers
                
        cdef float[3] centre
               
        tensor3d=self.df_to_tensor_strides(df)
        
        cdef double[:,:,:] tensor3d_view = tensor3d
        
        cusum=0
        
        nc=self.ncells
        pwr=self.power
        pgid_to_longlat=self.pgid_to_longlat
        pgid_to_index=self.pgid_to_index
        
        for p in range(pwr+1):
            powers_view[p]=(2**p)**3
            cusum+=powers_view[p]
            cupowers_view[p]=cusum
        
        # dry run through tree build to count number of nodes required

        # create array of zeros which will be used to indicate which of all the possible 
        # nodes in a with a leaf node grid of size ncells x ncells x ncells are actually 
        # needed 
          
        nodes_provisional_count=numpy.array([0 for i in range(cupowers_view[-1])])
        
        cdef long[:] nodes_provisional_count_view = nodes_provisional_count
        
        nodes_provisional_count_view[0]=1
        
        ntimes=len(times)
        
        # first, populate leaf nodes
        
        nleaf=0
        
        for itime in range(ntimes):        
            
            time=times[itime]

            timeoffset=time*nc*nc
        
            for pgid in pgids:
                nleaf+=1
                ipgid=pgid_to_index[pgid]

                ix,iy=pgid_to_longlat[pgid]
              
                levelindex=ix+iy*nc
                
                masterindex=cupowers_view[-2]+timeoffset+levelindex
            
                nodes_provisional_count_view[masterindex]=1

        # now populate lower levels

        for p in range(pwr-1,0,-1):

            istart=cupowers_view[p]
            iend=cupowers_view[p+1]
            
            ncellsp=2**p
            ncellsp2=ncellsp*ncellsp
            
            ncellsp1=2**(p+1)
            ncellsp12=ncellsp1*ncellsp1
            
            nodesize=nc/ncellsp

            for inode in range(istart,iend):

                if nodes_provisional_count_view[inode]==1:

                    inodelevel=inode-istart
                    
                    it=int(inodelevel/ncellsp12)
                    
                    ispace=inodelevel-it*ncellsp12
                    
                    iy=int(ispace/ncellsp1)

                    ix=ispace-iy*ncellsp1

                    ix2=ix/2
                    iy2=iy/2
                    if p==(pwr-1):
                        it2=(it-1)/2
                    else:
                        it2=it/2

                    levelindex=ix2+iy2*ncellsp
                    timeoffset=it2*ncellsp2
                
                    masterindex=cupowers_view[p-1]+levelindex+timeoffset        

                    nodes_provisional_count_view[masterindex]=1
                
        # build dicts to translate a nodes position in the master list of all possible
        # nodes to the actual compactified list of required nodes        
        
        inode_to_master={}
        master_to_inode={}
        
        inode=0
        for imaster in range(cupowers_view[-1]):
            if nodes_provisional_count_view[imaster]==1:
                inode_to_master[inode]=imaster
                master_to_inode[imaster]=inode
                inode+=1   
        
        # count numbers of nodes actually required and generate a list of 'blank' nodes
        # to fill in during the real tree build
        
        nnodes=numpy.count_nonzero(nodes_provisional_count)    

        nodes=numpy.array([None for i in range(nnodes)])

        centre=[-1,-1,-1]

        for inode in range(nnodes):
            node=SpaceTimeNode(-1,-1,-1,-1,-1,-1,-1,-1,centre,-1,-1,-1,-1)
            nodes[inode]=node
		
        
        cdef SpaceTimeNode[:] nodes_view = nodes
        
        # begin real tree build
                 
        # populate leaf nodes
        
        inode=nnodes-nleaf
        
        istart=inode
        
        nleafnodes=0
        
        for itime in range(ntimes):
        
            time=times[itime]
                
            timeoffset=time*nc*nc
        
            for pgid in pgids:
            
                ipgid=pgid_to_index[pgid]
                
                feature=tensor3d_view[itime,ipgid,0]

                ix,iy=pgid_to_longlat[pgid]

                node=nodes_view[inode]

                centre=[ix+0.5,iy+0.5,time-0.5]
                    
                node.masterindex=inode
                node.level=pwr
                node.left=ix
                node.right=ix+1
                node.bottom=iy
                node.top=iy+1
                node.past=time-1
                node.future=time
                node.centre=centre
                node.isleaf=1
                node.pgid=pgid
                node.time=time
                node.feature=feature
                node.nleaf=1
                                       
                nleafnodes+=1
                inode+=1

        # populate lower levels
        
        self.nleafnodes=nleafnodes
        
        for p in range(pwr-1,0,-1):

            istart=cupowers_view[p]
            iend=cupowers_view[p+1]
            
            ncellsp=2**p
            ncellsp2=ncellsp*ncellsp
            nodesize=nc/ncellsp
            mult=float(ncellsp)/float(nc)
            for imaster in range(istart,iend):
        
                 if nodes_provisional_count_view[imaster]==1:
                    inode=master_to_inode[imaster]
                    node=nodes_view[inode]

                    fix,fiy,fit=node.centre

                    ix=int(fix*mult)
                    iy=int(fiy*mult)
                    it=int(fit*mult)

                    levelindex=ix+iy*ncellsp
                    timeoffset=it*ncellsp2
                
                    masterindex=cupowers_view[p-1]+levelindex+timeoffset
                
                    iparent=master_to_inode[masterindex]
                    
                    parent=nodes_view[iparent]
                
                    if parent.nleaf==0:
                      
                        left=ix*nodesize
                        right=left+nodesize
                        bottom=iy*nodesize
                        top=bottom+nodesize
                        past=it*nodesize
                        future=past+nodesize
                      
                        centre=[(left+right)/2,(bottom+top)/2,(past+future)/2]
                      
                        parent.masterindex=iparent
                        
                        parent.level=p
                        parent.left=left
                        parent.right=right
                        parent.bottom=bottom
                        parent.top=top
                        parent.past=past
                        parent.future=future
                        parent.centre=centre
                        parent.isleaf=0
                        parent.pgid=-1
                        parent.time=-1
                        parent.nchild=0
                        parent.children[parent.nchild]=node.masterindex
                        parent.nchild+=1
                        parent.nleaf+=node.nleaf
                        parent.feature+=node.feature
                        
                        node.parent=parent.masterindex
                        
                    else:
                
                        parent.children[parent.nchild]=node.masterindex
                        parent.nchild+=1
                        parent.nleaf+=node.nleaf
                        parent.feature+=node.feature
                        
                        node.parent=parent.masterindex
                    
        # create root node
        
        left=0
        right=nc
        bottom=0
        top=nc
        past=0
        future=nc
        
        centre=[nc/2,nc/2,nc/2]
        
        root=nodes_view[0]

        root.masterindex=0
        root.level=0
        root.left=left
        root.right=right
        root.bottom=bottom
        root.top=top
        root.past=past
        root.future=future
        root.centre=centre
        root.isleaf=0
        root.pgid=-1
        root.time=-1
        root.nchild=0
        
        for ichild in range(1,9):
            child=nodes_view[ichild]
            if child.nleaf!=0:
                
                root.children[root.nchild]=ichild
                
                root.nleaf+=child.nleaf
                root.feature+=child.feature
                
                root.nchild+=1
                
                child.parent=root.masterindex

        self.nodes=nodes

        return

    def walk(self,df,omegacrit,nu,timeweightfn,spaceweightfn,tscale=1.0,sscale=1.0):
    
        '''
	    walk
	   
	    This function generates the list of nodes any given node will import data from, 
	    when one lags variables using the tree, as well as weights based on the distance 
	    between nodes' centres.
	    
	    The arguments are 
	    
	    - omegacrit: solid angle used to decide if a candidate node should be added to a target 
	      node's interaction list, based on the size of the candidate node and
	      the distance between the candidate node and the target node 
	   
	    - nu: arbitrary weighting factor between spatial and temporal distances
	    
	    - timeweightfn: an integer which selects what weighting to apply to the temporal
	      part of the spacetime interval between nodes. Allowed choices are
	      
	          (i) 1: exponential, exp(-delta_t/tscale)
	          
	    - spaceweightfn: an integer which selects what weighting to apply to the spatial
	      part of the spacetime interval between nodes. Allowed choices are:
	      
	          (i) 1: power law index -1, (delta_r/rscale)^-1
	          
	          (ii) 2: power law index -1, (delta_r/rscale)^-2
	          
	    - tscale: timescale used in temporal weighting function
	    
	    - rscale: distance scale used in spatial weighting function
	   
	    '''
    
        cdef int i
        cdef int inode
        cdef int istart
        cdef int iend
        cdef int ichild
        cdef int nbuffer
        cdef int largeint
        cdef int nleafnodes
        cdef int nnodes
        cdef int nodestart
        cdef int npgids
        cdef int ntimes
        cdef int ipgid
        cdef int itime
        cdef int itargettime
        cdef int itargetpgid
        
        cdef float deltay
        cdef float deltax
        cdef float deltat
        cdef float ds
        cdef float omega
        cdef float targetx
        cdef float targety
        cdef float targett
        cdef float nodex
        cdef float nodey
        cdef float nodet
        cdef float nulocal
        cdef float omega2pi
        cdef float targetfuture
        cdef float tscale_local
        cdef float sscale_local
        
        cdef double dist_pow
        cdef double targ
        cdef double sparg
        
        cdef float deltas2
        cdef float deltat2
        cdef float deltar2
        cdef float deltar4
        
        cdef dict pgid_to_index
        cdef dict time_to_index
        
        cdef extern from "math.h":
            double exp(double x)
            
        cdef extern from "math.h":
            double log(double x) 

        cdef extern from "math.h":
            double pow(double x, double y)
        
        cdef SpaceTimeNode targetnode
        cdef SpaceTimeNode node
        
        cdef SpaceTimeNode[:] nodes
        
        cdef array.array int_array_template = array.array('i', [])
        cdef array.array float_array_template = array.array('f', [])
        
        nbuffer=10000000
        
        targetpos = array.clone(int_array_template, 3, zero=False)
        nodestodo = array.clone(int_array_template, nbuffer, zero=False)
        
        cdef int[:] nodestodo_view = nodestodo 
    
        omega2pi=omegacrit/numpy.pi
        nulocal=nu
        tscale_local=tscale
        sscale_local=sscale
        
        if timeweightfn==1:
            tfunction=exp
        else:
            print('Unrecognised time weighting function - setting to exponential')
            tfunction=exp
            
        if spaceweightfn==1:
            sfunction=pow
            dist_pow=-0.5
        elif spaceweightfn==2:
            sfunction=pow
            dist_pow=-1.0
        else:
            print('Unrecognised space weighting function - setting to r^-2')
            sfunction=pow
            dist_pow=-1.0
           
    
        nleafnodes=self.nleafnodes
        nodes=self.nodes
        
        cdef SpaceTimeNode[:] nodes_view = nodes
        
        nnodes=len(nodes_view)
        
        pgid_to_index=self.pgid_to_index
        time_to_index=self.time_to_index
        
        npgids=len(self.pgids)
        ntimes=len(self.times)
        
        tensor3d=numpy.zeros((ntimes,npgids,1))
        
        cdef double[:,:,:] tensor3d_view = tensor3d

        for inode in range(nnodes-1,nnodes-(nleafnodes),-1):

            targetnode=nodes_view[inode]
                            
            targetx,targety,targett=targetnode.centre
            
            targetfuture=targetnode.future
            
            itargettime=targetnode.time
            itargetpgid=targetnode.pgid
            
            itime=time_to_index[itargettime]
            ipgid=pgid_to_index[itargetpgid]

            istart=1
            iend=9 
            for i in range(istart,iend):
                 nodestodo_view[i]=i
    
            while(istart<iend):
            
                nodestart=nodestodo_view[istart]
                node=nodes_view[nodestart]

                istart+=1
                
                if node.past>targetfuture:
                    continue
                
                nodex,nodey,nodet=node.centre

                deltax=targetx-nodex
                deltay=targety-nodey
                deltat=targett-nodet
                
                deltas2=deltax*deltax+deltay*deltay

                deltat=nulocal*deltat 
                
                if node.isleaf==1:
                    if node.future<=targetfuture:

                        targ=-(deltat+0.5)/tscale_local
                        sparg=(deltas2+0.5)/sscale_local

                        tensor3d_view[itime,ipgid,0]+=node.feature*tfunction(targ)*sfunction(sparg,dist_pow)
                    continue
       
                ds=node.top-node.bottom

                deltat2=deltat*deltat
                    
                deltar2=deltas2+deltat2
                
                deltar4=deltar2*deltar2
                
                omega=(deltas2*nulocal+deltat2)*ds*ds/deltar4

                if omega>omega2pi:
                # split node

                    for ichild in node.children:
                        if ichild==-1:break
                        
                        if ichild!=inode:          
                            nodestodo_view[iend]=ichild
                            iend+=1
                        
                else:
                    if node.future<=targetfuture:
                    
                        targ=-(deltat+0.5)/tscale_local
                        sparg=(deltas2+0.5)/sscale_local

                        tensor3d_view[itime,ipgid,0]+=node.feature*tfunction(targ)*sfunction(sparg,dist_pow)
                    continue
                    
    
        # create tensor to pack into df
    
        flat=numpy.empty((ntimes*npgids,1))
    
        for ichunk in range(ntimes):
            flat[ichunk*npgids:(ichunk+1)*npgids,:]=tensor3d_view[ichunk,:,:]
       
        feature=df.columns[0]
       
        df_column_names=[feature+'_spt_tr_om_'+str(omegacrit)+'_nu_'+str(nu)+'_tfn_'+str(timeweightfn)+'_tsc_'+str(tscale)+'_sfn_'+str(spaceweightfn)+'_ssc_'+str(sscale),]
        
        df_index=df.index
    
        df_treelags=pandas.DataFrame(flat, index=df_index, columns=df_column_names)

        return df_treelags
        
        
    def df_to_tensor_strides(self,df):
        '''
        df_to_tensor created 13/03/2021 by Jim Dale
        Uses as_strided from numpy stride_tricks library to create a tensorlike
        from a dataframe.
    
        dim0 of the tensor corresponds to level 0 of the df multiindex,
        dim1 corresponds to level 1 of the df multiindex, and dim2 corresponds to 
        the df's columns.
        '''

        # get shape of dataframe

        dim0,dim1=df.index.levshape
    
        dim2=df.shape[1]
    
        # check that df can in principle be tensorised
    
        if dim0*dim1!=df.shape[0]:
            raise Exception("df cannot be cast to a tensor - dim0 * dim1 != df.shape[0]",dim0,dim1,df.shape[0])

        flat=df.to_numpy()

        # get strides (in bytes) of flat array
        flat_strides=flat.strides

        offset2=flat_strides[1]

        offset1=flat_strides[0]
    
        # compute stride in bytes along dimension 0
        offset0=dim1*offset1

        # get memory view or copy as a numpy array
        tensor3d=numpy.lib.stride_tricks.as_strided(flat,shape=(dim0,dim1,dim2),
                                           strides=(offset0,offset1,offset2))
                                           
        return tensor3d   