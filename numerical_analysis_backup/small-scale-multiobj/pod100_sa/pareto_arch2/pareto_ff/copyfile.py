# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

#dirname = os.path.dirname(os.path.realpath(__file__))
dirname=''
for i in range(20):
    src = os.path.join(dirname, 'template_runsimu_connections.py')
    dst = 'pareto'+str(i)+'.py'
    dst = os.path.join(dirname, dst)
    
    newline = "i = "+str(i)+" \n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l!=22:
            destination.write(line)
        else:
            destination.write(newline)
    source.close()
    destination.close()
    
# bash files
for i in range(20):
    src = os.path.join(dirname, 'template_runsimu_connections.sh')
    dst = 'pareto'+str(i)+'.sh'
    dst = os.path.join(dirname, dst)
    
    newline3 = "#SBATCH -J pareto_pod100_"+str(i)+"\n"
    newline6 = "#SBATCH -o pareto_pod100_"+str(i)+".stdout\n"
    newline7 = "#SBATCH -e pareto_pod100_"+str(i)+".stderr\n"
    newline17 = "pdcp pareto"+str(i)+".py $TMPDIR\n"
    newline21 = "python pareto"+str(i)+".py\n"
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
    line = 'sbatch pareto'+str(i)+'.sh\n'
    f.write(line)
f.close()