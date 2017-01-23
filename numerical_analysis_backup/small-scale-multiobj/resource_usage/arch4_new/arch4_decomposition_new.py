# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:14:12 2016

@author: li
"""

from gurobipy import *
import numpy as np
import time
import itertools
import csv

class Arch4_decompose(object):
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
        self.slot_capacity = slot_capacity*num_cores
        # number of slot as guardband
        self.num_guard_slot = num_guard_slot
        # number of slots
        self.num_slots = num_slots
        # number of cores
        self.num_cores = 1
        # number of total demands
        self.total_demands = sum(self.traffic_matrix.flatten()>0)
        # weight factor
        self.alpha = alpha
        self.beta = beta
        
    def create_model_routing(self, **kwargs):
        """ILP
        """
        c_max = self.num_slots * self.slot_capacity
        self.tm = self.traffic_matrix.copy()
        # number of blocked demands at the begining
        self.num_blocked2 = sum(self.tm.flatten()>c_max)
        # remove those demands with too large capacities
        self.tm[self.tm>c_max] = 0
        
        # Model data
        # set of pods, pod_0, ..., pod_(N_p-1)
        pods = list(range(self.num_pods))
        # pairs of traffic demands
        traffic_pairs = tuplelist([(i, j) for i in pods for j in pods
                            if self.tm[i, j]>0])
        # traffic capacities
        traffic_capacities = {}
        for u in traffic_pairs:
            if self.tm[u[0],u[1]] > 0:
                traffic_slot = int(np.ceil(float(self.tm[u[0],u[1]]) / 
                            self.slot_capacity) + self.num_guard_slot)
                traffic_capacities[u] = traffic_slot
#                print(traffic_slot)
                
        # set of cores
        cores = list(range(self.num_cores))
        
        # Model
        tic = time.clock()
        model = Model('Arch4_routing')
        
        # binary variable: c_i,u,k = 1 if connection u uses core k in POD i
        core_usage = {}
        for u in traffic_pairs:
            for k in cores:
                for i in u:
                    core_usage[u,i,k] = model.addVar(vtype=GRB.BINARY)
                    
        suc = {}
        for u in traffic_pairs:
            suc[u] = model.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))
                    
        model.update()
        
        # one connection uses one core
        for u in traffic_pairs:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in cores)==suc[u])
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in cores)==suc[u])
            
        # flow per core
        for i in pods:
            tmp = list((i, j) for (i, j) in traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for k in cores:
                model.addConstr(quicksum(traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=self.num_slots)

        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
        toc = time.clock()
        
        self.model_routing = model
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
                
        suclist = [] # set of successfully allocated connections
        for u in self.traffic_pairs:
            if suc[u].x==1:
               suclist.append(u)
        self.suclist = suclist
        
        core_usagex = {} # core allocation
        for u in traffic_pairs:
            if u in suclist:
                for i in u:
                    for k in cores:
                        if core_usage[u,i,k].x==1:
                            core_usagex[u,i] = k
                            break
            else:
                core_usagex[u,u[0]] = -1
                core_usagex[u,u[1]] = -1
        self.core_usagex = core_usagex
        
        self.connections_ub = len(self.suclist)
        self.throughput_ub = sum(self.tm[u[0],u[1]] for u in self.suclist)
                    
    def create_model_sa(self, **kwargs):
        """Spectrum assignment ILP
        """

        smallM = self.num_slots
        bigM = 10*smallM
        
        # Model
        tic = time.clock()
        model_sa = Model('Arch4_sa')

        # binary variable: spectrum order
        spec_order = {}
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    spec_order[c[0],c[1]] = model_sa.addVar(vtype=GRB.BINARY)
        
        # continuous variable: first spectrum slot index
        # binary: fail?
        spec_idx = {}
        isfail = {}
        for u in self.suclist:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model_sa.update()
        
        # constraints: order
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset[i,k],2):
                    model_sa.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)
                    
        for u in self.suclist:
            model_sa.addConstr(bigM*isfail[u]>=
            spec_idx[u]+self.traffic_capacities[u]-smallM)

        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_sa.params, key, value)
                
        model_sa.optimize()
        toc = time.clock()
        
        self.model_sa = model_sa
        self.runtime_sa = toc-tic
        
        
        tmp = list(self.suclist)
        for u in self.suclist:
            if isfail[u].x == 1:
                tmp.remove(u)
        self.suclist_sa = tmp
        
        self.spec_idxx = {} # spectrum slots allocation
        for u in self.traffic_pairs:
            if u in self.suclist:
                self.spec_idxx[u] = spec_idx[u].x
            else:
                self.spec_idxx[u] = -1
                self.core_usagex[u,u[0]] = -1
                self.core_usagex[u,u[1]] = -1
        self.connections_lb = len(self.suclist_sa)
        self.throughput_lb = sum(self.tm[u[0],u[1]] for u in self.suclist_sa)
            
        # construct the resource tensor and list
        tensor_milp = np.ones((self.num_pods, self.num_cores, self.num_slots))
        for u in self.suclist_sa:
            src = u[0]
            dst = u[1]
            core_src = int(round(self.core_usagex[u,src]))
            core_dst = int(round(self.core_usagex[u,dst]))
            spec_idx = int(round(self.spec_idxx[u]))
            spec_bd = int(round(self.traffic_capacities[u]))
            res_src = tensor_milp[src,core_src,spec_idx:(spec_idx+spec_bd)]
            res_dst = tensor_milp[dst,core_dst,spec_idx:(spec_idx+spec_bd)]
            if (sum(res_src)==spec_bd) and (sum(res_dst)==spec_bd):
                res_src[:] = 0
                res_dst[:] = 0
        self.tensor_milp = tensor_milp
        self.efficiency_milp = (float(sum(self.tm[i] for i in self.suclist_sa))/
            sum(self.traffic_capacities[i]*self.slot_capacity 
            for i in self.suclist_sa))
            
    def write_result_csv(self, file_name, suclist):
        with open(file_name, 'w') as f:
            f.write("src,dst,spec,used_slot,tfk_slot\n")
            for u in suclist:
                wstr = "{},{},{},{},{}\n".format(u[0], u[1], self.spec_idxx[u], 
                                 self.traffic_capacities[u],
                                 np.ceil(float(self.tm[u])/self.slot_capacity))
                f.write(wstr)
                
    def one_runs(self, a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(a, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges[:,1] = ranges[:,1]-ranges[:,0]
        return ranges  
                
    def sa_heuristic(self, ascending1=False, ascending2=True):
        """
        """
        suclist = list(self.suclist)
        suclist_tm = [self.traffic_capacities[u] for u in suclist]
        if ascending1:
            suclist = [x for (y,x) in sorted(zip(suclist_tm, suclist))]
        else:
            suclist = [x for (y, x) in sorted(zip(suclist_tm, suclist), reverse=True)]
            
        IS_list = {} # independent set
        IS_list[0] = []
        cl_list = {}
        cl_list[0] = set()
        i = 0
        while len(suclist):
            tmplist = list(suclist)
            for u in tmplist:
                src = u[0]
                dst = u[1]
                src_core = self.core_usagex[u,src]
                dst_core = self.core_usagex[u,dst]
                if ((src,src_core) not in cl_list[i]) and ((dst, dst_core) not in cl_list[i]):
                    # add connection if it's independent to element in IS_list[i]
                    IS_list[i].append(u)
                    cl_list[i].add((src,src_core))
                    cl_list[i].add((dst,dst_core))
                    tmplist.remove(u)
            i += 1
            IS_list[i] = []
            cl_list[i] = set()
            suclist = tmplist

        del cl_list[i]
        del IS_list[i]

        self.obj_sah_ = 0
        self.obj_sah_connection_ = 0
        self.obj_sah_throughput_ = 0
        suclist = []
        restensor = np.ones((self.num_pods, self.num_cores, self.num_slots))        
        for i in range(len(IS_list)):
            for u in IS_list[i]:
                src = u[0]
                dst = u[1]
                src_core = self.core_usagex[u,src]
                dst_core = self.core_usagex[u,dst]
                tmpsrc = restensor[src,src_core,:]
                tmpdst = restensor[dst,dst_core,:]
                tmp = tmpsrc*tmpdst
                tmpavail = self.one_runs(tmp)
                tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                if tmpidx.size:
                   spec_idx = tmpavail[tmpidx[0],0]
                   restensor[src,src_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   restensor[dst,dst_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                   self.obj_sah_connection_ += 1
                   self.obj_sah_throughput_ += self.tm[src,dst]
                   suclist.append(u)

        remain_cnk = [u for u in self.traffic_pairs if u not in suclist]
        remain_tm = [self.traffic_capacities[u] for u in remain_cnk]
        if ascending2:
            remain_cnk = [x for (y,x) in sorted(zip(remain_tm,remain_cnk))]
        else:
            remain_cnk = [x for (y,x) in sorted(zip(remain_tm,remain_cnk), reverse=False)]

        for u in remain_cnk:
            src = u[0]
            dst = u[1]
            tmpsrc = restensor[src,:,:]
            tmpdst = restensor[dst,:,:]
            tmpcmb = np.zeros((self.num_cores**2, self.num_slots))
            k = 0
            avail_slots = {}
            for ksrc in self.cores:
                for kdst in self.cores:
                    tmpcmb[k,:] = tmpsrc[ksrc,:]*tmpdst[kdst,:]
                    tmpavail = self.one_runs(tmpcmb[k,:])
                    tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                    if not tmpidx.size:
                        avail_slots[ksrc,kdst] = np.array([-1, self.num_slots+1])
                    else:
                        idxm = np.argmin(tmpavail[tmpidx,1])
                        avail_slots[ksrc,kdst] = np.array(tmpavail[tmpidx[idxm],:])
                    k += 1
            avail_slots = list(sorted(avail_slots.iteritems(), key=lambda (x,y):y[1]))
            # avail_slots[0] has the form of ((core_out,core_in), [spec_idx,available_slots])
            if avail_slots[0][1][1]<=self.num_slots:
                src_core = avail_slots[0][0][0]
                dst_core = avail_slots[0][0][1]
                spec_idx = avail_slots[0][1][0]
                spec_bd = self.traffic_capacities[u]
                restensor[src,src_core,spec_idx:(spec_idx+spec_bd)] = 0
                restensor[dst,dst_core,spec_idx:(spec_idx+spec_bd)] = 0
                self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                self.obj_sah_connection_ += 1
                self.obj_sah_throughput_ += self.tm[src,dst]
                suclist.append(u)
        self.tensor_heuristic = restensor
        self.efficiency_heuristic = (float(sum(self.tm[i] for i in suclist))/
            sum(self.traffic_capacities[i]*self.slot_capacity 
            for i in suclist))
        self.suclist_heuristic = suclist

    def save_tensor(self, tensor, filename):
        tmp = tensor.reshape((-1, self.num_slots))
        np.savetxt(filename, tmp, fmt='%1d', delimiter=',')

#if __name__=='__main__':
#    from sdm1 import Traffic
#    np.random.seed(2010)
#    
#    #%% generate traffic
#    num_pods=100
#    max_pod_connected=20
#    min_pod_connected=10
#    mean_capacity=200
#    variance_capacity=100
#    num_cores=3
#    num_slots=80
#    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
#                min_pod_connected=min_pod_connected, 
#                mean_capacity=mean_capacity, 
#                variance_capacity=variance_capacity)
#    t.generate_traffic()
#    tm = t.traffic_matrix
#    
#    #%% read from file
#    filename = 'traffic_matrix__matrix_0.csv'
#    #    print filename
#    tm = []
#    with open(filename) as f:
#        reader = csv.reader(f)
#        for idx, row in enumerate(reader):
#            if idx>11:
#                row.pop()
#                row = [int(u) for u in row]
#                tm.append(row)
#    tm = np.array(tm)*25
#    #%% optimize    
#    m = Arch4_decompose(tm, num_slots=num_slots, num_cores=num_cores, alpha=1, beta=0.01)
#    m.create_model_routing(mipfocus=1,timelimit=100)
##    m.create_model_sa(mipfocus=1,timelimit=100)
#    m.sa_heuristic(ascending1=False,ascending2=True)
#    print float(m.obj_sah_connection_)/m.connections_ub
#    print float(m.obj_sah_throughput_)/m.throughput_ub