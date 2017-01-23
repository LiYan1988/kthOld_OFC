# -*- coding: utf-8 -*-
"""
Created on Mon May 23 21:05:47 2016

@author: li

solve routing problem in arch2
"""

import pandas as pd
from gurobipy import *
from scipy.linalg import toeplitz
import numpy as np
import time
import itertools
import operator
import matplotlib.pyplot as plt
from sdm1 import Traffic
from arch2 import ModelSDM_arch2

class Arch2_decompose(object):
    """Create models for different SDM DCN architectures
    """
    def __init__(self, traffic_matrix, num_slots=320, num_cores=10,
                 slot_capacity =25, num_guard_slot=1):
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
        
    def routing_model(self, **kwargs):
        """ILP
        """
        c_max = self.num_slots * self.slot_capacity
        self.tm_arch2 = self.traffic_matrix.copy()
        # number of blocked demands at the begining
        self.num_blocked2 = sum(self.tm_arch2.flatten()>c_max)
        # remove those demands with too large capacities
        self.tm_arch2[self.tm_arch2>c_max] = 0
        
        # Model data
        # set of pods, pod_0, ..., pod_(N_p-1)
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
                            if self.tm_arch2[i, j]>0])
        # traffic capacities
        traffic_capacities = {}
        for u in traffic_pairs:
            if self.tm_arch2[u[0],u[1]] > 0:
                traffic_slot = int(np.ceil(self.tm_arch2[u[0],u[1]] / 
                            self.slot_capacity) + self.num_guard_slot)
                traffic_capacities[u] = traffic_slot
#                print(traffic_slot)
                
        # set of cores
        cores = list(range(self.num_cores))
        
        # Model
        tic = time.clock()
        model = Model('Arch2_routing')
        
        # binary variable: c_i,u,k = 1 if connection u uses core k in POD i
        core_usage = {}
        for u in traffic_pairs:
            for k in cores:
                for i in u:
                    core_usage[u,i,k] = model.addVar(vtype=GRB.BINARY)
                    
        flow = {}
        for i in pods:
            for k in cores:
                flow[i,k] = model.addVar(vtype=GRB.CONTINUOUS)
                
        flow_max = {}
        for i in pods:
            flow_max[i] = model.addVar(vtype=GRB.CONTINUOUS, obj=1)
            
#        flow_mm = model.addVar(vtype=GRB.CONTINUOUS, obj=1)
        
        model.update()
        
        # one connection uses one core
        for u in traffic_pairs:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in cores)==1)
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in cores)==1)
            
        # flow per core
        for i in pods:
            tmp = list((i, j) for (i, j) in traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for k in cores:
                model.addConstr(quicksum(#traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)==flow[i,k])
                model.addConstr(flow[i,k]<=flow_max[i])
#                model.addConstr(flow[i,k]<=flow_mm)
                
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
        toc = time.clock()
        
        self.model = model
        self.runtime = toc-tic
        self.pods = pods
        self.cores = cores
        self.traffic_pairs = traffic_pairs
        self.traffic_capacities = traffic_capacities
        
        pcset = {} # set of connections using pod i, core k
        for i in pods:
            for k in cores:
                pcset[i,k] = set()
                
        for u in traffic_pairs:
            for k in cores:
                for i in u:
                    if core_usage[u,i,k].x==1:
                        pcset[i,k].add(u)
                        
        self.pcset = pcset
                
        self.flow = flow
        self.flow_max = flow_max
        self.core_usage = core_usage
        
        
    def sa_model(self, **kwargs):
        """Spectrum assignment ILP
        """

        smallM = self.num_slots
        bigM = 10*smallM
        
        # Model
        tic = time.clock()
        model_sa = Model('Arch2_sa')
        
        # binary variable: spectrum order
        spec_order = {}
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    spec_order[c[0],c[1],0] = model_sa.addVar(vtype=GRB.BINARY)
                    spec_order[c[0],c[1],1] = model_sa.addVar(vtype=GRB.BINARY)
                    
        # continuous variable: first spectrum slot index
        # binary: fail?
        spec_idx = {}
        isfail = {}
        for u in self.traffic_pairs:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=1)
            
        model_sa.update()
        
        # constraints: order
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    model_sa.addConstr(spec_order[c[0],c[1],0]+
                    spec_order[c[0],c[1],1]==1)
                    model_sa.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1],0]<=bigM)
                    model_sa.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*spec_order[c[0],c[1],1]<=bigM)
                    
        for u in self.traffic_pairs:
            model_sa.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-1-smallM)
            
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_sa.params, key, value)
                
        model_sa.optimize()
        toc = time.clock()
        
        self.model_sa = model_sa
        self.runtime_sa = toc-tic
#        for u in self.traffic_pairs:
#            print(spec_idx[u].x)
        
    def sa_heu1(self):
        """find independent sets, and allocate
        """
        pairs = self.traffic_capacities
        pairs_sorted = sorted(pairs.items(), key=operator.itemgetter(1))
        pairs_core_out = {}
        pairs_core_in = {}
        for u in self.traffic_pairs:
            for k in self.cores:
                if u in self.pcset[u[0],k]:
                    pairs_core_out[u]=k
                if u in self.pcset[u[1],k]:
                    pairs_core_in[u]=k
                    
        pairs = []
        
        for i in range(len(self.traffic_pairs)):
            tmp = pairs_sorted[i][0]
            pairs.append(tmp+(pairs_core_out[tmp],)+(pairs_core_in[tmp],)+(pairs_sorted[i][1],))
            
        # (src, dst, src core, dst core, slots)
        self.pairs = pairs
#        pairs.reverse()
        
        resource = np.zeros((self.num_pods, self.num_cores, self.num_slots), dtype=bool)
        self.n_blk=0
        self.ffis(resource, pairs)
        self.resource = resource
        
    def ffis0(self, resource, pairs):
        for c in pairs:
            src = c[0]
            dst = c[1]
            csrc = c[2]
            cdst = c[3]
            slots = c[4]
            spec_src = resource[src,csrc,:]
            spec_dst = resource[dst,cdst,:]
            spec = spec_src+spec_dst
            ranges = self.zero_runs(spec, slots)
            if sum(ranges)!=-3:
                resource[src,csrc,ranges[0]:(ranges[0]+slots)] = True
                resource[dst,cdst,ranges[0]:(ranges[0]+slots)] = True
            else:
                self.n_blk += 1
        
    def ffis(self, resource, pairs):
        """First-fit with independent sets"""
        islist = self.find_is(pairs)
        for c in islist:
            src = c[0]
            dst = c[1]
            csrc = c[2]
            cdst = c[3]
            slots = c[4]
            spec_src = resource[src,csrc,:]
            spec_dst = resource[dst,cdst,:]
            spec = spec_src+spec_dst
            ranges = self.zero_runs(spec, slots)
            if sum(ranges)!=-3:
                resource[src,csrc,ranges[0]:(ranges[0]+slots)] = True
                resource[dst,cdst,ranges[0]:(ranges[0]+slots)] = True
            else:
                self.n_blk += 1
        print(self.n_blk)
        if len(pairs)>0:
            self.ffis(resource, pairs)
            
        
    def zero_runs(self, a, c):
        """Find the holes in link spectrum
        
        a: the link spectrum
        c: the capacity of the traffic demand
        """
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
        absdiff = np.abs(np.diff(iszero))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges = np.hstack((ranges, np.diff(ranges)))
        idx = np.where(ranges[:,-1] >= c)[0]
        if len(idx):
            ranges = ranges[idx[0], :]
        else:
            ranges = np.array([-1, -1, -1])
        return ranges
        
        
    def find_is(self, inlist):
        """find a independent set in inlist"""
        ind = np.random.randint(0, len(inlist)-1)
        print(ind)
        tmplist = [inlist[ind]]
        del inlist[ind]
        stop = False
        while stop==False:
            ind = self.find_ic(tmplist, inlist)
            if ind!=-1:
                tmplist.append(inlist[ind])
                del inlist[ind]
            else:
                stop = True
        
        return tmplist
        
    def find_ic(self, tmplist, inlist):
        """find one connection independent with tmplist in inlist"""
        for n,i in enumerate(inlist):
            isfind=True
            for j in tmplist:
                iset = set([i[0]*self.num_cores+i[2], i[1]*self.num_cores+i[3]])
                jset = set([j[0]*self.num_cores+j[2], j[1]*self.num_cores+j[3]])
                if len(iset.intersection(jset))!=0:
                    isfind=False
                    break
            if isfind:
                return n

        return -1
        


if __name__=='__main__':
    np.random.seed(2010)
    
    #%% generate traffic
    num_pods=50
    max_pod_connected=250
    min_pod_connected=150
    mean_capacity=100
    variance_capacity=200
    num_cores=3
    num_slots=160
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
                min_pod_connected=min_pod_connected, 
                mean_capacity=mean_capacity, 
                variance_capacity=variance_capacity)
    t.generate_traffic()
    tm = t.traffic_matrix
    
    #%% read from file
#    tm = pd.read_csv('simu1_matrix_1.csv',skiprows=12,header=None)
#    tm.dropna(axis=1, how='any', inplace=True)
#    tm = tm.as_matrix()*25

    #%% optimize    
    m = Arch2_decompose(tm, num_slots=num_slots, num_cores=num_cores)
    m.routing_model(mipfocus=1,timelimit=1000)
    m.sa_model(mipfocus=1,timelimit=1000)
    
#    flow = np.zeros((m.num_pods, m.num_cores))
#    for i in m.pods:
#            for k in m.cores:
#                flow[i,k] = m.flow[i,k].x
        
#    coreplt = {}
#    fig, ax = plt.subplots(figsize=(30, 30))
#    width = 0.7/num_cores
#    for k in m.cores:
#        ind = m.pods
#        ind = [u+k*width for u in ind]
#        coreplt[k] = ax.bar(ind, flow[:,k], width, color='r', edgecolor='r')
#        
#    plt.savefig('result.pdf', bbox_inches='tight')