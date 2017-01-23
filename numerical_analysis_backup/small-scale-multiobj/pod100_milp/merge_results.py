# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 15:05:18 2016

@author: li

merge simulation results 
"""

import os
import shutil
import tempfile
import numpy as np
import operator

def merge(csv_path, typ):
    os.chdir(csv_path+'/'+typ)

    file_list = os.listdir(os.getcwd())

    result_files = [u for u in file_list if u.split('_')[0]=='result']
    result_files = sorted(result_files, key=lambda x: int(x.split('_')[2].split('to')[0]))
    start_end = np.zeros((len(result_files), 2), dtype=int)
    csv_file = '../results_'+typ+'.csv'
    with open(csv_file, 'w') as dst:
        for i, u in enumerate(result_files):
            tmp = u.split('_')[2].split('to')
            start_end[i, 0] = int(tmp[0])
            start_end[i, 1] = int(tmp[1].split('.')[0])
            with open(u,'r') as src:
                if i == 0:
                    line = next(src)
                    line = 'id,'+line
                    dst.write(line)
                    for j in range(start_end[i,0], start_end[i,1]):
                        line = next(src)
                        line = str(j)+','+line
                        dst.write(line)
                else:
                    next(src)
                    for j in range(start_end[i,0], start_end[i,1]):
                        line = next(src)
                        line = str(j)+','+line
                        dst.write(line)
    

if __name__=="__main__":
    # change directory
    # os.chdir('/home/li/Dropbox/KTH/numerical_analysis/small-scale-multiobj/pod100_milp')
    csv_path = os.getcwd()
    typ1 = 'connections'
    typ2 = 'throughput'
    typ3 = 'hybrid'
    merge(csv_path, typ1)
    merge(csv_path, typ2)
    merge(csv_path, typ3)
