# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:27:05 2016

@author: li
"""

import os

#dirname = os.path.dirname(os.path.realpath(__file__))
dirname=''
for i in range(2,21):
    src = os.path.join(dirname, 'core1.cpp')
    dst = 'core'+str(i)+'.cpp'
    dst = os.path.join(dirname, dst)
    
    newline1 = "        num_cores = "+str(i)+"+id;\n"
    newline2 = '    string filename = "result_test2_core'+str(i)+'.csv";\n'
    destination = open( dst, "w" )
    source = open( src, "r" )
    for l, line in enumerate(source):
        if l!=34 and l!=61:
            destination.write(line)
        elif l==34:
            destination.write(newline1)
        elif l==61:
            destination.write(newline2)
    source.close()
    destination.close()
    
# bash files
#for i in range(20):
#    src = os.path.join(dirname, 'arch2.sh')
#    dst = 'arch2_'+str(i)+'_pod125.sh'
#    dst = os.path.join(dirname, dst)
#    
#    newline3 = "#SBATCH -J simu2_arch2_"+str(i)+":\n"
#    newline6 = "#SBATCH -o simu2_arch2_"+str(i)+"_output.stdout\n"
#    newline7 = "#SBATCH -e simu2_arch2_"+str(i)+"_output.stderr\n"
#    newline13 = "pdcp arch2_"+str(i)+"_pod125.py simu2_matrix_"+str(i)+".csv $TMPDIR\n"
#    newline17 = "python arch2_"+str(i)+"_pod125.py\n"
#    destination = open( dst, "w" )
#    source = open( src, "r" )
#    for l, line in enumerate(source):
#        if l==3:
#            destination.write(newline3)
#        elif l==6:
#            destination.write(newline6)
#        elif l==7:
#            destination.write(newline7)
#        elif l==13:
#            destination.write(newline13)
#        elif l==17:
#            destination.write(newline17)
#        else:
#            destination.write(line)
#    source.close()
#    destination.close()
