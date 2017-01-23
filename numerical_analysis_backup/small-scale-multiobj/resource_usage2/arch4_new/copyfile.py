# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

betav = [0,1e-5,1e-4, 5e-4, 1e-3, 3e-3, 5e-3, 0.01, 0.1, 1]
dirname=''
for i, b in enumerate(betav):
    src = os.path.join(dirname, 'template.py')
    dst = 'ru_arch4_'+str(i)+'.py'
    dst = os.path.join(dirname, dst)
    
    newline = "beta = "+str(b)+" \n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l!=28:
            destination.write(line)
        else:
            destination.write(newline)
    source.close()
    destination.close()
    
# bash files
for i,b in enumerate(betav):
    src = os.path.join(dirname, 'template.sh')
    dst = 'ru_arch4_'+str(i)+'.sh'
    dst = os.path.join(dirname, dst)
    
    newline3 = "#SBATCH -J ru_arch4_new_"+str(i)+"\n"
    newline6 = "#SBATCH -o ru_arch4_new_"+str(i)+".stdout\n"
    newline7 = "#SBATCH -e ru_arch4_new_"+str(i)+".stderr\n"
    newline17 = "pdcp ru_arch4_"+str(i)+".py $TMPDIR\n"
    newline21 = "python ru_arch4_"+str(i)+".py\n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l==3:
            destination.write(newline3)
        elif l==6:
            destination.write(newline6)
        elif l==7:
            destination.write(newline7)
        elif l==17:
            destination.write(newline17)
        elif l==21:
            destination.write(newline21)
        else:
            destination.write(line)
    source.close()
    destination.close()
    
f = open('run_sbatch.txt', 'w')
for i, b in enumerate(betav):
    line = 'sbatch ru_arch4_'+str(i)+'.sh\n'
    f.write(line)
f.close()