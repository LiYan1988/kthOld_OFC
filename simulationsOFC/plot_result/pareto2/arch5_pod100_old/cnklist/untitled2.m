clc;
close all;
clear;

beta = [0;1e-05;2e-05;4e-05;8e-05;0.0001;0.0002;0.0004;0.0008;...
    0.001;0.002;0.004;0.008;0.01;0.02;0.04;0.08;0.1;0.2;0.4;1;10];
thp = zeros(20,22);
cnk = zeros(20,22);
for j = 1:20
    for i = 1:22
        b = beta(i);
        filename = sprintf('cnklist_heuristic_%d_%.2e.csv',j-1, b);
        [src,dst1,spec,slots_used,core_src,core_dst,cores_used,tfk_slot] = importCnklist(filename);
        x = importCnkMat(filename);
        y = sum(abs(diff(x, 1, 1)),2);
        idx = [1;find(y)+1];
        thp(j,i)=sum(tfk_slot(idx));
        cnk(j,i)=length(tfk_slot(idx));
    end
end
save('cnklistResult.mat', 'thp', 'cnk')