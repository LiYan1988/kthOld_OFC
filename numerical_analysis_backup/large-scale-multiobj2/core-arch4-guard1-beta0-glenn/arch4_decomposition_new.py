# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:53:44 2016

@author: li
"""

from gurobipy import *
import numpy as np
import time
import itertools
#from sdm1 import Traffic
import copy
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
        
        self.pods = pods
        self.traffic_pairs = traffic_pairs
        self.traffic_capacities = traffic_capacities
        self.cores = cores
        
    def create_model_routing(self, **kwargs):
        """ILP
        """
        # Model
        tic = time.clock()
        model = Model('Arch4_routing')
        
        # binary variable: c_i,u,k = 1 if connection u uses core k in POD i
        core_usage = {}
        for u in self.traffic_pairs:
            for k in self.cores:
                for i in u:
                    core_usage[u,i,k] = model.addVar(vtype=GRB.BINARY)
                  
        # the absolute difference between the core index chosen by a traffic
#        core_diff = {}
#        for u in self.traffic_pairs:
#            for k in self.cores:
#                core_diff[u] = model.addVar(vtype=GRB.INTEGER, obj=0.1)
                    
        suc = {}
        for u in self.traffic_pairs:
            suc[u] = model.addVar(vtype=GRB.BINARY, obj=-(self.alpha+self.beta*self.tm[u[0],u[1]]))

        model.update()
        
        # one connection uses one core
        for u in self.traffic_pairs:
            model.addConstr(quicksum(core_usage[u,u[0],k] for k in self.cores)==suc[u])
            model.addConstr(quicksum(core_usage[u,u[1],k] for k in self.cores)==suc[u])
            
        # flow per core
        for i in self.pods:
            tmp = list((i, j) for (i, j) in self.traffic_pairs.select(i, '*'))
            tmp0 = list((j, i) for (j, i) in self.traffic_pairs.select('*', i))
            tmp.extend(tmp0)
            for k in self.cores:
                model.addConstr(quicksum(self.traffic_capacities[u]*
                core_usage[u, i, k] for u in tmp)<=self.num_slots)

        # limit core switches
#        for u in self.traffic_pairs:
#            model.addConstr(core_diff[u] >= 
#                quicksum(core_usage[u,u[0],k] for k in self.cores)-
#                quicksum(core_usage[u,u[1],k] for k in self.cores))
#            model.addConstr(core_diff[u] >= 
#                quicksum(core_usage[u,u[0],k] for k in self.cores)-
#                quicksum(core_usage[u,u[1],k] for k in self.cores))
        
        # params
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model.params, key, value)
        
        model.optimize()
        toc = time.clock()
        
        self.model_routing = model
        self.runtime = toc-tic
        
        pcset = {} # set of connections using pod i, core k
        for i in self.pods:
            for k in self.cores:
                pcset[i,k] = []
        
        for u in self.traffic_pairs:
            for k in self.cores:
                for i in u:
                    if core_usage[u,i,k].x==1:
                        pcset[i,k].append(u)
        self.pcset_dc = pcset
                
        suclist = [] # set of successfully allocated connections
        for u in self.traffic_pairs:
            if suc[u].x==1:
               suclist.append(u)
        self.suclist_dc = suclist
        
        core_usagex = {} # core allocation
        for u in self.traffic_pairs:
            if u in suclist:
                for i in u:
                    for k in self.cores:
                        if core_usage[u,i,k].x>=0.9:
                            core_usagex[u,i] = k
                            break
            else:
                core_usagex[u,u[0]] = -1
                core_usagex[u,u[1]] = -1
        self.core_usagex = core_usagex
        
        self.connection_ub_ = len(suclist)
        self.throughput_ub_ = sum(self.tm[u[0],u[1]] for u in self.suclist_dc)
        self.obj_ub_ = self.alpha*self.connection_ub_+self.beta*self.throughput_ub_
                
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
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    spec_order[c[0],c[1]] = model_sa.addVar(vtype=GRB.BINARY)
        
        # continuous variable: first spectrum slot index
        # binary: fail?
        spec_idx = {}
        isfail = {}
        for u in self.suclist_dc:
            spec_idx[u] = model_sa.addVar(vtype=GRB.CONTINUOUS)
            isfail[u] = model_sa.addVar(vtype=GRB.BINARY, obj=self.alpha+self.beta*self.tm[u[0],u[1]])
            
        model_sa.update()
        
        # constraints: order
        for i in self.pods:
            for k in self.cores:
                for c in itertools.combinations(self.pcset_dc[i,k],2):
                    model_sa.addConstr(spec_idx[c[0]]+self.traffic_capacities[c[0]]-
                    spec_idx[c[1]]+bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(spec_idx[c[1]]+self.traffic_capacities[c[1]]-
                    spec_idx[c[0]]+bigM*(1-spec_order[c[0],c[1]])<=bigM)

        for u in self.suclist_dc:
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
        
        tmp = list(self.suclist_dc)
        for u in self.suclist_dc:
            if isfail[u].x == 1:
                tmp.remove(u)
        self.suclist_sa = tmp
        
        self.spec_idxx = {} # spectrum slots allocation
        for u in self.traffic_pairs:
            if u in self.suclist_dc:
                self.spec_idxx[u] = int(round(spec_idx[u].x))
            else:
                self.spec_idxx[u] = -1
                self.core_usagex[u,u[0]] = -1
                self.core_usagex[u,u[1]] = -1                
            self.connection_lb_ = len(self.suclist_sa)
            self.throughput_lb_ = sum(self.tm[u[0],u[1]] for u in self.suclist_sa)

        # construct the resource tensor
        self.cnklist_sa = []
        tensor_milp = np.ones((self.num_pods, self.num_cores, self.num_slots), dtype=np.int8)
        for u in self.suclist_sa:
            src = u[0]
            dst = u[1]
            core_src = self.core_usagex[u,src]
            core_dst = self.core_usagex[u,dst]
            spec_idx = self.spec_idxx[u]
            spec_bd = self.traffic_capacities[u]
            tmp = [src, dst, spec_idx, spec_bd, core_src, core_dst, self.tm[u]]
            self.cnklist_sa.append(tmp)
            res_src = tensor_milp[src,core_src,spec_idx:(spec_idx+spec_bd)]
            res_dst = tensor_milp[dst,core_dst,spec_idx:(spec_idx+spec_bd)]
            if (sum(res_src)==spec_bd) and (sum(res_dst)==spec_bd):
                res_src[:] = 0
                res_dst[:] = 0
        self.tensor_milp = tensor_milp
        self.efficiency_milp = (float(sum(self.tm[i] for i in self.suclist_sa))/
            sum(self.traffic_capacities[i]*self.slot_capacity 
            for i in self.suclist_sa))
        self.obj_lb_ = self.alpha*self.connection_lb+self.beta*self.throughput_lb
            
    def write_result_csv(self, file_name, suclist):
        with open(file_name, 'w') as f:
            f.write('src,dst,spec,slots_used,core_src,core_dst,tfk_slot\n')
            for c in suclist:
                wstr = '{},{},{},{},{},{},{}\n'.format(c[0], c[1], c[2], 
                    c[3], c[4], c[5], c[6])
                f.write(wstr)

    def one_runs(self, a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(a, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges[:,1] = ranges[:,1]-ranges[:,0]
        return ranges  
                        
    def check(self, cnklist):
        """Check feasibility of solution
        """
        # check if any two connections are overlapped
        n_overlap=0
        for (u,v) in itertools.combinations(cnklist,2):
            if set(u)&set(v):
                cout_u = self.cnk_resource[u][2]
                cin_u = self.cnk_resource[u][3]
                si_u = self.cnk_resource[u][1]
                sb_u = self.traffic_capacities[u]

                cout_v = self.cnk_resource[v][2]
                cin_v = self.cnk_resource[v][3]
                si_v = self.cnk_resource[v][1]
                sb_v = self.traffic_capacities[v]
                
                if set([(u[0], cout_u), (u[1], cin_u)])&set([(v[0], cout_v), (v[1], cin_v)]):
                    if (si_u>=si_v and si_v+sb_v-1>=si_u) or (si_v>=si_u and si_u+sb_u-1>=si_v):
                        print [(u[0], cout_u), (u[1], cin_u)]
                        print [(v[0], cout_v), (v[1], cin_v)]
                        print 'wrong'
                        n_overlap+=1
        
        # check if any connection is out of range 
        n_oof = 0
        for u in self.cnk_group_suc:
            si = self.cnk_resource[u][1]
            sb = self.traffic_capacities[u]
            if si+sb-1>self.num_slots:
                n_oof+=1
        return (n_overlap, n_oof)
        
    def sa_heuristic(self, ascending1=True,ascending2=True):
        """Spectrum assignment heuristi
        ascending1: order of allocating connections in suclist
        ascending2: order of allocating connections in remain list
        """
        suclist = list(self.suclist_dc)
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
        cnklist = []
        restensor = np.ones((self.num_pods, self.num_cores, self.num_slots),dtype=np.int0)        
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
                   tmp = [src, dst, spec_idx, self.traffic_capacities[u], 
                      src_core, dst_core, self.tm[u]]
                   cnklist.append(tmp)
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
                tmp = [src, dst, spec_idx, self.traffic_capacities[u], 
                   src_core, dst_core, self.tm[u]]
                cnklist.append(tmp)
        self.tensor_heuristic = restensor
#        self.efficiency_heuristic = (float(sum(self.tm[i] for i in suclist))/
#            sum(self.traffic_capacities[i]*self.slot_capacity 
#            for i in suclist))
        self.suclist_heuristic = cnklist
        
    def sa_heuristic_aff(self, ascending=True):
        """First fit with optimized core allocation
        """
        # ordering the connections
        suclist = list(self.suclist_dc)
        suclist_tm = [self.traffic_capacities[u] for u in suclist]
        if ascending:
            suclist = [x for (y,x) in sorted(zip(suclist_tm, suclist))]
        else:
            suclist = [x for (y, x) in sorted(zip(suclist_tm, suclist), reverse=True)]
        
        # first fit
        restensor = np.ones((self.num_pods, self.num_cores, self.num_slots), dtype=np.int0)
        self.obj_affopt_ = 0
        self.obj_affopt_connection_ = 0
        self.obj_affopt_throughput_ = 0
        self.cnklist_affopt = [] # list of successfully allocated connections
        for i,u in enumerate(suclist):
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
               self.obj_affopt_ += self.alpha+self.beta*self.tm[src,dst]
               self.obj_affopt_connection_ += 1
               self.obj_affopt_throughput_ += self.tm[src,dst]
               tmp = [src, dst, spec_idx, self.traffic_capacities[u], 
                      src_core, dst_core, self.tm[u]]
               self.cnklist_affopt.append(tmp)
        
    def heuristic(self):
        objbest = 0
        objcnk = 0
        objthp = 0
        cnklist = []
        self.sa_heuristic(ascending1=True, ascending2=True)
        if objbest < self.obj_sah_:
            objbest = self.obj_sah_
            objcnk = self.obj_sah_connection_
            objthp = self.obj_sah_throughput_
            cnklist = self.suclist_heuristic
        self.sa_heuristic(ascending1=True, ascending2=False)
        if objbest < self.obj_sah_:
            objbest = self.obj_sah_
            objcnk = self.obj_sah_connection_
            objthp = self.obj_sah_throughput_
            cnklist = self.suclist_heuristic
        self.sa_heuristic(ascending1=False, ascending2=True)
        if objbest < self.obj_sah_:
            objbest = self.obj_sah_
            objcnk = self.obj_sah_connection_
            objthp = self.obj_sah_throughput_
            cnklist = self.suclist_heuristic
        self.sa_heuristic(ascending1=False, ascending2=False)
        if objbest < self.obj_sah_:
            objbest = self.obj_sah_
            objcnk = self.obj_sah_connection_
            objthp = self.obj_sah_throughput_
            cnklist = self.suclist_heuristic
            
        self.sa_heuristic_aff(ascending=True)
        if objbest < self.obj_affopt_:
            objbest = self.obj_affopt_
            objcnk = self.obj_affopt_connection_
            objthp = self.obj_affopt_throughput_
            cnklist = self.cnklist_affopt
        self.sa_heuristic_aff(ascending=False)
        if objbest < self.obj_affopt_:
            objbest = self.obj_affopt_
            objcnk = self.obj_affopt_connection_
            objthp = self.obj_affopt_throughput_
            cnklist = self.cnklist_affopt
            
        self.aff(ascending=True)
        if objbest < self.obj_aff_:
            objbest = self.obj_aff_
            objcnk = self.obj_aff_connection_
            objthp = self.obj_aff_throughput_
            cnklist = self.cnklist_aff
        self.aff(ascending=False)
        if objbest < self.obj_aff_:
            objbest = self.obj_aff_
            objcnk = self.obj_aff_connection_
            objthp = self.obj_aff_throughput_
            cnklist = self.cnklist_aff
        
        self.obj_heuristic_ = objbest
        self.obj_heuristic_connection_ = objcnk
        self.obj_heuristic_throughput_ = objthp
        self.cnklist_heuristic_ = cnklist
        
    def aff(self, ascending=True):
        """First fit according to the given connection list
        """
        suclist = list(self.traffic_pairs)
        suclist_tm = [self.traffic_capacities[u] for u in suclist]
        if ascending:
            suclist = [x for (y,x) in sorted(zip(suclist_tm, suclist))]
        else:
            suclist = [x for (y, x) in sorted(zip(suclist_tm, suclist), reverse=True)]
        
        restensor = np.ones((self.num_pods, self.num_cores, self.num_slots), dtype=np.int0)
        self.obj_aff_ = 0
        self.obj_aff_connection_ = 0
        self.obj_aff_throughput_ = 0
        self.cnklist_aff = []
        for i,u in enumerate(suclist):
            src = u[0]
            dst = u[1]
            core_candidates = [(x,y) for x in self.cores for y in self.cores]
            for src_core, dst_core in core_candidates:
                tmpsrc = restensor[src,src_core,:]
                tmpdst = restensor[dst,dst_core,:]
                tmp = tmpsrc*tmpdst
                tmpavail = self.one_runs(tmp)
                tmpidx = np.where(tmpavail[:,1]>=self.traffic_capacities[u])[0]
                if tmpidx.size:
                   spec_idx = tmpavail[tmpidx[0],0]
                   restensor[src,src_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   restensor[dst,dst_core,spec_idx:(spec_idx+self.traffic_capacities[u])] = 0
                   self.obj_aff_ += self.alpha+self.beta*self.tm[src,dst]
                   self.obj_aff_connection_ += 1
                   self.obj_aff_throughput_ += self.tm[src,dst]
                   tmp = [src, dst, spec_idx, self.traffic_capacities[u], 
                          src_core, dst_core, self.tm[u]]
                   self.cnklist_aff.append(tmp)
                   break
                
    def save_tensor(self, tensor, filename):
        """Save resource tensor
        save as csv
        """
        tmp = tensor.reshape((-1, self.num_slots))
        np.savetxt(filename, tmp, fmt='%1d',delimiter=',')
        # for load the saved tensor
        # tmp = np.loadtxt(filename, delimiter=',')
        # tensor = tmp.reshape((self.num_pods, self.num_cores, self.num_slots))

if __name__=='__main__':
    np.random.seed(2014)
    
    #%% generate traffic
    num_pods=100
    max_pod_connected=300
    min_pod_connected=150
    mean_capacity=200
    variance_capacity=100
    num_cores=3
    num_slots=80
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
    m = Arch4_decompose(tm, num_slots=num_slots, num_cores=num_cores, alpha=1, beta=0.0)
    
    #%% test heuristic
    m.create_model_routing(mipfocus=1,timelimit=100,mipgap=0.1,method=2) # Method=2 or 3
#    m.create_model_sa(mipfocus=1,timelimit=100,method=2,SubMIPNodes=2000,
#                      Heuristics=0.8)
    m.heuristic()
    m.write_result_csv('test.csv',m.cnklist_heuristic_)
    print m.obj_ub_
    print m.obj_heuristic_
#    #    m.create_model_sa(mipfocus=1,timelimit=40)
#    m.create_model_partition_heuristic(6,2,timelimit=400,mipgap=0.5) # timelimit=120 is enough
#    # submatrices    
#    sa_flag = 0
#    m.create_model_group(num_slots, sa_flag, mipfocus_r=1, timelimit_r=180, mipgap_r=0.05, 
#                         mipfocus_s=1,timelimit_s=180, mipgap_s=0.2) 
#    # routing solved instantly, sa uses 180 and stopped prematurely
#
#    m.create_model_subgroup_offdiag(mipfocus_soff=1,timelimit_soff=180,mipgap=0.01) 
#    # solved instantly
#
#    print m.obj_connections_
#    print m.obj_throughput_
#    print m.check()
    
#    m.create_model_routing_group(15, timelimit=100, mipfocus=1, mipgap=0.1)
#    print m.alpha*m.connections_ub+m.beta*m.throughput_ub
    # optimal: 154574, 2: 130496.55, 5: 129383.02, 10: 145800.58, 15: 145156.37, 

#    m.create_model_routing_group(10, timelimit=100, mipfocus=1, mipgap=0.1)
#    m.create_model_partition_heuristic(10,2,timelimit=400,mipgap=0.5) # timelimit=120 is enough
#    sa_flag=0
#    m.create_model_group(num_slots, sa_flag, mipfocus_r=1, timelimit_r=180, mipgap_r=0.05, 
#                     mipfocus_s=1,timelimit_s=300, mipgap_s=0.1) # sa should run long enough time
#    m.create_model_subgroup_offdiag(mipfocus_soff=1,timelimit_soff=180,mipgap_soff=0.01) 
#    print m.obj_connections_ / float(m.connections_ub)
#    print m.obj_throughput_ / float(m.throughput_ub)
#    print m.check()