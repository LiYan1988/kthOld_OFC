clc;
close all;
clear;

for i =0:19
    filename1 = sprintf('result_pareto_arch4_pod100_nf_%d.csv',i);
    filename2 = sprintf('1_result_pareto_arch4_pod100_nf_%d.csv',i);
    movefile(filename1, filename2);
end