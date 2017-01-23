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
                        
        core_usagex = {}
        for u in self.traffic_pairs:
            if is_suc[u].x==1:
                chout = core_choicex[u,u[0]]
                chin = core_choicex[u,u[1]]
                core_out = np.where(B[:,chout]==1)[0]
                core_in = np.where(B[:,chin]==1)[0]
                core_usagex[u,u[0]] = core_out
                core_usagex[u,u[1]] = core_in
                        
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
        self.core_usagex = core_usagex
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
            for k in self.cores:
                for c in itertools.combinations(self.cnk_in_core[i,k],2):
                    model_sa.addConstr(
                    spec_idx[c[0]]+self.nslot_choice[c[0]]-spec_idx[c[1]]+
                    bigM*spec_order[c[0],c[1]]<=bigM)
                    model_sa.addConstr(
                    spec_idx[c[1]]+self.nslot_choice[c[1]]-spec_idx[c[0]]+
                    bigM*(1-spec_order[c[0],c[1]])<=bigM)

        for u in self.suclist:
            model_sa.addConstr(
            bigM*isfail[u]>=spec_idx[u]+self.nslot_choice[u]-smallM)
            
        if len(kwargs):
            for key, value in kwargs.items():
                setattr(model_sa.params, key, value)
                
        model_sa.optimize()
        
        self.model_sa = model_sa
          
        tmp = list(self.suclist)
        for u in self.suclist:
            if isfail[u].x==1:
                tmp.remove(u)
        self.suclist_sa = list(tmp)

        self.spec_idxx = {}
        for u in self.suclist:
            self.spec_idxx[u] = spec_idx[u].x

        self.connections_lb = len(self.suclist)           
        self.throughput_lb = sum(self.tm[u[0],u[1]] for u in self.suclist)
        
        # construct the resource tensor
        tensor_milp = np.ones((self.num_pods, self.num_cores, self.num_slots))
        for u in self.suclist_sa:
            src = u[0]
            dst = u[1]
            core_src = self.core_usagex[u,src]
            core_dst = self.core_usagex[u,dst]
            spec_idx = int(round(self.spec_idxx[u]))
            spec_bd = int(round(self.nslot_choice[u]))
            res_src = tensor_milp[src,core_src,spec_idx:(spec_idx+spec_bd)]
            res_dst = tensor_milp[dst,core_dst,spec_idx:(spec_idx+spec_bd)]
            if (np.sum(res_src)==spec_bd*core_src.size) and (np.sum(res_dst)==spec_bd*core_dst.size):
                tensor_milp[src,core_src,spec_idx:(spec_idx+spec_bd)] = 0
                tensor_milp[dst,core_dst,spec_idx:(spec_idx+spec_bd)] = 0
        self.tensor_milp = tensor_milp
        self.efficiency_milp = (float(sum(self.tm[i] for i in self.suclist_sa))/
            sum(self.nslot_choice[i]*self.core_usagex[i,i[0]].size*self.slot_capacity 
            for i in self.suclist_sa))
            
            
    def write_result_csv(self, file_name, suclist):
        with open(file_name, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'spec', 'core_src', 
                             'core_dst', '#core', 'used_slot', 'tfk_slot'])
            for u in suclist:
                col_src = [self.B[j,self.core_choice[u,u[0]]] for j in self.cores]
                core_src = self.one_runs(col_src)[0][0]
                col_dst = [self.B[j,self.core_choice[u,u[1]]] for j in self.cores]
                core_dst = self.one_runs(col_dst)[0][0]
                num_cores = self.one_runs(col_dst)[0][1]
                used_slot = self.nslot_choice[u]
                tfk_slot = np.ceil(float(self.tm[u])/self.slot_capacity)
                writer.writerow([u[0],u[1],
                                 self.spec_idxx[u],core_src,core_dst,num_cores,
                                 used_slot,tfk_slot])
        
    def sa_heuristic(self, ascending1=False, ascending2=True):
        """
        """
        suclist = list(self.suclist)
        suclist_tm = [self.nslot_choice[u] for u in suclist]
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
                src_core = list(self.core_usagex[u,src])
                dst_core = list(self.core_usagex[u,dst])
                srct = set(zip([src]*len(src_core),src_core))
                dstt = set(zip([dst]*len(dst_core),dst_core))
                sdset = srct|dstt
                if len(sdset-cl_list[i])==len(sdset):
                    # add connection if it's independent to element in IS_list[i]
                    IS_list[i].append(u)
                    cl_list[i].update(sdset)
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
                tmpsrc = np.prod(restensor[src,src_core,:],axis=0,dtype=bool)
                tmpdst = np.prod(restensor[dst,dst_core,:],axis=0,dtype=bool)
                tmp = tmpsrc*tmpdst
                tmpavail = self.one_runs(tmp)
                tmpidx = np.where(tmpavail[:,1]>=self.nslot_choice[u])[0]
                if tmpidx.size:
                   spec_idx = tmpavail[tmpidx[0],0]
                   restensor[src,src_core,spec_idx:(spec_idx+self.nslot_choice[u])] = False
                   restensor[dst,dst_core,spec_idx:(spec_idx+self.nslot_choice[u])] = False
                   self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                   self.obj_sah_connection_ += 1
                   self.obj_sah_throughput_ += self.tm[src,dst]
                   suclist.append(u)

        remain_cnk = [u for u in self.traffic_pairs if u not in suclist]
        remain_tm = [self.tm[u]/float(self.slot_capacity) for u in remain_cnk]
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
                    tmpidx = np.where(tmpavail[:,1]>=self.tm[u]*self.slot_capacity)[0]
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
                spec_bd = self.nslot_choice[u]
                restensor[src,src_core,spec_idx:(spec_idx+spec_bd)] = 0
                restensor[dst,dst_core,spec_idx:(spec_idx+spec_bd)] = 0
                self.obj_sah_ += self.alpha+self.beta*self.tm[src,dst]
                self.obj_sah_connection_ += 1
                self.obj_sah_throughput_ += self.tm[src,dst]

    def one_runs(self, a):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(a, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        ranges[:,1] = ranges[:,1]-ranges[:,0]
        return ranges  
        
    def save_tensor(self, tensor, filename):
        """Save resource tensor
        save as csv
        """
        tmp = tensor.reshape((-1, self.num_slots))
        np.savetxt(filename, tmp, fmt='%1d',delimiter=',')


if __name__=='__main__':
    from sdm1 import Traffic
    np.random.seed(2010)
    
    #%% generate traffic
    num_pods=250
    max_pod_connected=int(num_pods*0.5)
    min_pod_connected=1
    mean_capacity=200
    variance_capacity=200
    num_cores=10
    num_slots=320
    
    t = Traffic(num_pods=num_pods, max_pod_connected=max_pod_connected, 
            min_pod_connected=min_pod_connected, 
            mean_capacity=mean_capacity, 
            variance_capacity=variance_capacity)
    t.generate_traffic()
    tm = t.traffic_matrix

#    tmdf = pd.DataFrame(tm)
#    tmdf.to_csv('tm_arch5.csv', header=False, index=False)

    #%% read from file
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

    #%% optimize
    m = Arch5_decompose(tm, num_slots=num_slots, num_cores=num_cores, alpha=1, beta=0.01)
    m.create_model_routing(mipfocus=1, timelimit=1000, method=2, mipgap=0.02)
    m.create_model_sa(mipfocus=1,timelimit=1000, method=2, SubMIPNodes=2000, Heuristics=0.8)
    print m.connections_lb/float(m.connections_ub)
    print m.throughput_lb/float(m.throughput_ub)
#    m.sa_heuristic(ascending1=True, ascending2=True)
#    print float(m.obj_sah_connection_)/m.connections_ub
#    print float(m.obj_sah_throughput_)/m.throughput_ub