# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

#dirname = os.path.dirname(os.path.realpath(__file__))
dirname=''
for i in range(20):
    src = os.path.join(dirname, 'template1.py')
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
    
    newline3 = "#SBATCH -J core_arch5_"+str(i)+"\n"
    newline7 = "#SBATCH -o core_arch5_"+str(i)+".stdout\n"
    newline8 = "#SBATCH -e core_arch4_"+str(i)+".stderr\n"
    newline15 = "pdcp pareto"+str(i)+".py $TMPDIR\n"
    newline19 = "python pareto"+str(i)+".py\n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l==3:
            destination.write(newline3)
        elif l==7:
            destination.write(newline7)
        elif l==8:
            destination.write(newline8)
        elif l==15:
            destination.write(newline15)
        elif l==19:
            destination.write(newline19)
        else:
            destination.write(line)
    source.close()
    destination.close()
    
f = open('run_sbatch.txt', 'w')
for i in range(20):
    line = 'sbatch pareto'+str(i)+'.sh\n'
    f.write(line)
f.close()