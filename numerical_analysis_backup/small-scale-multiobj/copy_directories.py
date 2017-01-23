# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 15:05:18 2016

@author: li

prepare files for pod150_milp and pod200_milp
"""

import os
import shutil
import tempfile

def change_line(file_path, line_number, newline):
    # create temp file
    fh, abs_path = tempfile.mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for l, line in enumerate(old_file):
                if l == line_number:
                    new_file.write(newline)
                else:
                    new_file.write(line)
    os.close(fh)
    # remove original file
    os.remove(file_path)
    # move new file
    shutil.move(abs_path, file_path)

def replace(file_path, old_pattern, new_pattern):
    # create temp file
    fh, abs_path = tempfile.mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(old_pattern, new_pattern))

    os.close(fh)
    # remove old file
    os.remove(file_path)
    # move new file
    shutil.move(abs_path, file_path)
    
def prepare_files(npod, typ):
    """
    Prepare files for MILP simulations
    npod: number of PODs (150 or 200)
    typ: type of optimization (hybrid or connections or throughput)
    """
    os.chdir('/home/li/Dropbox/KTH/numerical_analysis/small-scale-multiobj')
    
    file_path = 'pod'+str(npod)+'_milp'
    
    # # remove directory if it exists
    # if os.path.exists(file_path):
    #     shutil.rmtree(file_path)
        
    # # create new directory
    # os.mkdir(file_path)
        
    # # copy all files from pod100_milp/
    # os.system('cp -rf pod100_milp/* '+file_path+'/')
    
    # generate traffic matrices
    os.chdir(file_path+'/'+typ+'/')
    
    # modify generate_traffic_matrices.cpp
    file_path = 'generate_traffic_matrices.cpp'
    line_number = 13
    newline = '    int num_pods = '+str(npod)+';\n'
    change_line(file_path, line_number, newline)
    
    line_number = 0
    newline = '#include "../../../heuristics/sa_sdm.h"\n'
    change_line(file_path, line_number, newline)
    
    # run generate_traffic_matrices.cpp
    os.system('g++ -std=c++11 -pthread generate_traffic_matrices.cpp -o main; ./main')

    # modify the python template
    file_path = 'template_runsimu_'+typ+'.py'
    line_number = 29
    if npod == 150:
        timelimit = 18000
    elif npod == 200:
        timelimit = 25200
    newline = 'time_limit_sa = '+str(timelimit)+'\n' # change gurobi running time
    change_line(file_path, line_number, newline)
    
    line_number = 6
    newline = 'optimize '+typ+'\n' # change comment
    change_line(file_path, line_number, newline)

    # change the bash template
    file_path = 'template_runsimu_'+typ+'.sh'
    old_pattern = 'pod100'
    new_pattern = 'pod'+str(npod)
    replace(file_path, old_pattern, new_pattern)
    
    file_path = 'copyfile.py'
    replace(file_path, old_pattern, new_pattern)

    # replicate the template
    os.system('python copyfile.py')
    
    

if __name__=="__main__":
    os.chdir('/home/li/Dropbox/KTH/numerical_analysis/small-scale-multiobj')

    #%% POD = 150
    # remove directory if it exists
    if os.path.exists('pod150_milp'):
        shutil.rmtree('pod150_milp')

    os.mkdir('pod150_milp')
       
    # copy all files from pod100_milp/
    os.system('cp -rf pod100_milp/* pod150_milp/')

    npod = 150
    typ1 = 'connections'
    typ2 = 'hybrid'
    typ3 = 'throughput'
    prepare_files(npod, typ1)
    prepare_files(npod, typ2)
    prepare_files(npod, typ3)

    os.chdir('/home/li/Dropbox/KTH/numerical_analysis/small-scale-multiobj')

    #%% POD = 200
    # remove directory if it exists
    if os.path.exists('pod200_milp'):
        shutil.rmtree('pod200_milp')

    os.mkdir('pod200_milp')
       
    # copy all files from pod100_milp/
    os.system('cp -rf pod100_milp/* pod200_milp/')

    npod = 200
    typ1 = 'connections'
    typ2 = 'hybrid'
    typ3 = 'throughput'
    prepare_files(npod, typ1)
    prepare_files(npod, typ2)
    prepare_files(npod, typ3)