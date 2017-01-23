# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:39:25 2016

@author: li
"""

from gurobipy import *
from scipy.linalg import toeplitz
import numpy as np
import time
import itertools
import csv

class Arch5_decompose(object):
    """Create models for different SDM DCN architectures
    """
    def __init__(self, traffic_matrix, num_slots=320, num_cores=10,
                 slot_capacity =25, num_guard_slot=1, alpha=1, beta=0):
        """Initialize 
        """
        # traffic matrix
        self.traffic_matrix = traffic_matrix
        # number of PODs
        self.num_pods = traffic_matrix.shape[0]
        # capacity per spectrum slot, Gbps
        self.slot_capacity = slot_capacity
        # number of slot as guardband
        self.num_guard_slot = num_guard_slot
        # number of slots
        self.num_slots = num_slots
        # number of cores
        self.num_cores = num_cores
        # number of total demands
        self.total_demands = sum(self.traffic_matrix.flatten()>0)
        
        
        # Need to consider guardbands, no need to consider max capacity 
        # since a traffic can use the whole fiber
        self.tm = self.traffic_matrix.copy()        
        # Model data
        # set of pods
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
                            if self.tm[i, j]>0])
        
        # Set of possible combinations of core and slot numbers
        core_set = {}
        slot_set = {}
        volu_set = {}
        for i, j in traffic_pairs:
            tmp = self.core_slot(self.tm[i, j])
            core_set[(i, j)] = tmp[:, 0]
            slot_set[(i, j)] = tmp[:, 1]
            volu_set[(i, j)] = tmp[:, 2]
        
        # set of cores
        cores = list(range(self.num_cores))
        
        self.pods = pods
        self.cores = cores
        self.core_set = core_set
        self.slot_set = slot_set
        self.volu_set = volu_set
        self.traffic_pairs = traffic_pairs
        # weight factor
        self.alpha = alpha
        self.beta = beta
        
    def volumn_model(self, **kwargs):
        """Estimate the volume of each connection, i.e., the combination of 
        core adn slot numbers.
        """
        # Model
        tic = time.clock()
        model_vol = Model('model_vol')
        
        # variable: choice of core-slot combination
        # variable: succuss?
        vol_choice = {}
        is_suc = {}
        vol_cnk = {}
        for u in self.traffic_pairs:
            is_suc[u] = model_vol.addVar(vtype=GRB.BINARY, obj=-1)
            vol_cnk[u] = model_vol.addVar(vtype=GRB.CONTINUOUS)
            for i in range(self.num_cores):
                vol_choice[u, i] = model_vol.addVar(vtype=GRB.BINARY, obj=-0.00001)
        
        # variable: volumn
        vol_limit = self.num_cores*self.num_slots
        vol_pod = {}
        for i in self.pods:
            vol_pod[i] = model_vol.addVar(vtype=GRB.CONTINUOUS, ub=vol_limit)
                
        model_vol.update()
        
        # constraints: success
        for u in self.traffic_pairs:
            model_vol.addConstr(quicksum(vol_choice[u, i] 
            for i in range(self.num_cores))==is_suc[u])
            model_vol.addConstr(quicksum(vol_choice[u, i]*self.volu_set[u][i]
            for i in range(self.num_cores))==vol_cnk[u])
                
        for i in self.pods:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i))
            # all the traffics in link i
            tmp.extend(tmp0)
            model_vol.addConstr(quicksum(vol_cnk[u] for u in tmp)==vol_pod[i])
        
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_vol.params, key, value)
        
        model_vol.optimize()
        toc = time.clock()
        
        is_sucx = {}
        for u in self.traffic_pairs:
            is_sucx[u] = is_suc[u].x
        vol_choicex = {}
        for u in self.traffic_pairs:
            for i in range(self.num_cores):
                if(vol_choice[u,i].x==1):
                    vol_choicex[u] = i
        self.is_suc = is_sucx
        self.vol_choice = vol_choicex
        
    def core_slot(self, capacity):
        """Find all the possible combination of core and slot numbers for 
        a traffic demand with given capacity
        The guardband is considered
        
        Output: m * 2 numpy array, the first column is the number of cores, 
        and the second column is the number of slots, m is the number of 
        possible combinations.
        """
        # total number of slots
        n_slots = np.ceil(capacity / self.slot_capacity)
        # list of all combinations of core and slot numbers
        combination = [] 
        for i in range(1, self.num_cores+1):
            u = [i,int(np.ceil(n_slots/i)+self.num_guard_slot)]
            u.append(u[0]*u[1])
            combination.append(tuple(u))
        combination = np.asarray(combination)
                
        return combination
        
    def create_model_routing(self, **kwargs):
        channels_core = []
        group_core = {}
        tmp = 0
        B = np.empty((self.num_cores, 0))
        for n in range(1, self.num_cores+1):
            channels_core.extend(list(range(tmp, tmp+self.num_cores-n+1)))
            group_core[n] = list(range(tmp, tmp+self.num_cores-n+1))
            tmp = tmp+self.num_cores-n+1
            c = np.zeros((self.num_cores,))
            c[:n] = 1
            r = np.zeros((self.num_cores-n+1))
            r[0] = 1
            B = np.hstack((B, toeplitz(c,r)))
        self.B = B
        self.channels_core = channels_core
        self.group_core = group_core
        
        channels_core_nslot = {}
        for u in self.traffic_pairs:
            for n in range(1, self.num_cores+1):
                for i in group_core[n]:
                    channels_core_nslot[u,i] = self.slot_set[u][n-1]

        model_routing = Model('model_routing')
    
        core_choice = {}
        for u in self.traffic_pairs:
            for i in channels_core:
                core_choice[u,u[0],i] = model_routing.addVar(vtype=GRB.BINARY)
                core_choice[u,u[1],i] = model_routing.addVar(vtype=GRB.BINARY)
                
        is_suc = {}
        for u in self.traffic_pairs:
            is_suc[u] = model_routing.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))
            
        flow_core = {}
        for i in self.pods:
            for j in self.cores:
                flow_core[i,j] = model_routing.addVar(vtype=GRB.CONTINUOUS, ub=self.num_slots)
        
        model_routing.update()
        
        for u in self.traffic_pairs:
            model_routing.addConstr(quicksum(core_choice[u,u[0],i] 
            for i in channels_core)==is_suc[u])
            model_routing.addConstr(quicksum(core_choice[u,u[1],i] 
            for i in channels_core)==is_suc[u])
            #core channel consistent
            for n in range(1, self.num_cores+1):
                model_routing.addConstr(quicksum(core_choice[u,u[0],i] for i in group_core[n]) 
                == quicksum(core_choice[u,u[1],i] for i in group_core[n]))
        
        
        for i in self.pods:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i))
            # all the traffics in link i
            tmp.extend(tmp0)
            for j in self.cores:
                model_routing.addConstr(quicksum(
                channels_core_nslot[u,k]*B[j,k]*core_choice[u,i,k]
                for k in channels_core
                for u in tmp)==flow_core[i,j])

        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_routing.params, key, value)
        
        model_routing.optimize()
        
        core_choicex = {} # which core channel
        nslot_choice = {} # number of spectral slots per core for connection u using channel i
        for u in self.traffic_pairs:
            if is_suc[u].x==1:
                for i in channels_core:
                    if core_choice[u,u[0],i].x==1:
                        core_choicex[u,u[0]] = i
                        nslot_choice[u] = channels_core_nslot[u,i]
                    if core_choice[u,u[1],i].x==1:
                        core_choicex[u,u[1]] = i
#                    core_usagex[u] = 
                
        is_sucx = {}
        for u in self.traffic_pairs:
            is_sucx[u] = is_suc[u].x
            
        flow_corex = {}
        for i in self.pods:
            for j in self.cores:
                flow_corex[i,j] = flow_core[i,j].x

        cnk_in_core = {} # set of connections using a particular core
        for i in self.pods:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i))
            # all the traffics in link i
            tmp.extend(tmp0)
            for j in self.cores:
                cnk_in_core[i,j] = []
                for u in tmp:
                    if sum(core_choice[u,i,k].x*B[j,k]for k in channels_core)==1:
                        cnk_in_core[i,j].append(u)
        
        suclist = []
        for u in self.traffic_pairs:
            if is_sucx[u]==1:
                suclist.append(u)
                
        self.core_choice = core_choicex
        self.is_suc_routing = is_sucx
        self.flow_core = flow_corex
        self.cnk_in_core = cnk_in_core
        self.suclist = suclist
        self.nslot_choice = nslot_choice
        self.n_suc_routing = len(suclist)
        self.model_routing = model_routing
        
        self.connections_ub = len(self.suclist)
        self.throughput_ub = sum(self.tm[u[0],u[1]] for u in self.suclist)
        

    def create_model_sa(self, **kwargs):
        smallM = self.num_slots
        bigM = 10*smallM
        
        model_sa = Model('model_sa')
        
        spec_order = {}
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.cnk_in_core[i,k],2):
                    spec_order[c[0],c[1]] = model_sa.addVar(vtype=GRB.BINARY)

        spec_idx = {}
        for u in self.suclist:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)

        isfail = {}
        for u in self.suclist:
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])

        model_sa.update()

        for i in self.pods:
            for j in self.cores:
                for c in itertools.combinations(self.cnk_in_core[i,k],2):
                    model_sa.addConstr(
                    spec_idx[c[0]]+self.nslot_choice[c[0]]-spec_idx[c[1]]+
                    bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(
                    spec_idx[c[1]]+self.nslot_choice[c[1]]-spec_idx[c[0]]+
                    bigM*(1-spec_order[c[0],c[1]])<=bigM)

        for u in self.suclist:
            model_sa.addConstr(
            bigM*isfail[u]>=spec_idx[u]+self.nslot_choice[u]-1-smallM)
            
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_sa.params, key, value)
                
        model_sa.optimize()
        
        self.model_sa = model_sa
        
        try:            
            for u in self.suclist:
                if isfail[u]==1:
                    self.suclist.remove(u)
                    
            self.spec_idxx = {}
            for u in self.suclist:
                self.spec_idxx[u] = spec_idx[u].x

            self.connections_lb = len(self.suclist)           
            self.throughput_lb = sum(self.tm[u[0],u[1]] for u in self.suclist)
        except:
            self.connections_lb = 0      
            self.throughput_lb = 0
            
    def write_result_csv(self, file_name):
        with open(file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'spec', 'core_src', 'core_dst', '#core'])
            for u in self.suclist:
                col_src = [self.B[j,self.core_choice[u,u[0]]] for j in self.cores]
                core_src = next((i for i, x in enumerate(col_src) if x), None)
                col_dst = [self.B[j,self.core_choice[u,u[1]]] for j in self.cores]
                core_dst = next((i for i, x in enumerate(col_dst) if x),None)
                writer.writerow([u[0],u[1],self.spec_idxx[u],core_src,core_dst,sum(col_src)])
                
    def one_runs(self, a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(a, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges[:,1] = ranges[:,1]-ranges[:,0]
        return ranges  
        

if __name__=='__main__':
    from sdm1 import Traffic
    np.random.seed(2010)
    
    #%% generate traffic
    num_pods=20
    max_pod_connected=20
    min_pod_connected=10
    mean_capacity=100
    variance_capacity=200
    num_cores=3
    num_slots=40
    
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
            min_pod_connected=min_pod_connected, 
            mean_capacity=mean_capacity, 
            variance_capacity=variance_capacity)
    t.generate_traffic()
    tm = t.traffic_matrix

#    tmdf = pd.DataFrame(tm)
#    tmdf.to_csv('tm_arch5.csv', header=False, index=False)

    #%% read from file
#    tm = pd.read_csv('simu1_matrix_1.csv',skiprows=12,header=None)
#    tm.dropna(axis=1, how='any', inplace=True)
#    tm = tm.as_matrix()*25

    #%% optimize    
    m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores, alpha=1, beta=0.01)
    m.create_model_routing(mipfocus=1, timelimit=10)
    m.create_model_sa(mipfocus=1, timelimit=40)
    m.write_result_csv('arch5.csv')
