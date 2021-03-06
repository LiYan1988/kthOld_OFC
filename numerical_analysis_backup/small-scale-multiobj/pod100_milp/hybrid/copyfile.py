# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

#dirname = os.path.dirname(os.path.realpath(__file__))
dirname=''
for i in range(20):
    src = os.path.join(dirname, 'template_runsimu_hybrid.py')
    dst = 'runsimu'+str(i)+'_hybrid.py'
    dst = os.path.join(dirname, dst)
    
    newline = "n_start = "+str(i)+" # index of start \n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l!=26:
            destination.write(line)
        else:
            destination.write(newline)
    source.close()
    destination.close()
    
# bash files
for i in range(20):
    src = os.path.join(dirname, 'template_runsimu_hybrid.sh')
    dst = 'runsimu'+str(i)+'_hybrid.sh'
    dst = os.path.join(dirname, dst)
    
    newline3 = "#SBATCH -J pod100_"+str(i)+"_hybrid\n"
    newline6 = "#SBATCH -o pod100_"+str(i)+"_hybrid.stdout\n"
    newline7 = "#SBATCH -e pod100_"+str(i)+"_hybrid.stderr\n"
    newline17 = "pdcp runsimu"+str(i)+"_hybrid.py $TMPDIR\n"
    newline21 = "python runsimu"+str(i)+"_hybrid.py\n"
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
for i in range(20):
    line = 'sbatch runsimu'+str(i)+'_hybrid.sh\n'
    f.write(line)
f.close()