# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

#dirname = os.path.dirname(os.path.realpath(__file__))
dirname=''
for i in range(20):
    src = os.path.join(dirname, 'arch2.py')
    dst = 'arch2_pod175_'+str(i)+'.py'
    dst = os.path.join(dirname, dst)
    
    newline = '    with open("simu4_matrix_'+str(i)+'.csv") as f:\n'
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l!=218:
            destination.write(line)
        else:
            destination.write(newline)
    source.close()
    destination.close()
    
# bash files
for i in range(20):
    src = os.path.join(dirname, 'arch2.sh')
    dst = 'arch2_pod175_'+str(i)+'.sh'
    dst = os.path.join(dirname, dst)
    
    newline3 = "#SBATCH -J simu4_arch2_"+str(i)+"\n"
    newline6 = "#SBATCH -o simu4_arch2_"+str(i)+"_output.stdout\n"
    newline7 = "#SBATCH -e simu4_arch2_"+str(i)+"_output.stderr\n"
    newline13 = "pdcp arch2_pod175_"+str(i)+".py simu4_matrix_"+str(i)+".csv $TMPDIR\n"
    newline17 = "python arch2_pod175_"+str(i)+".py\n"
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l==3:
            destination.write(newline3)
        elif l==6:
            destination.write(newline6)
        elif l==7:
            destination.write(newline7)
        elif l==13:
            destination.write(newline13)
        elif l==17:
            destination.write(newline17)
        else:
            destination.write(line)
    source.close()
    destination.close()