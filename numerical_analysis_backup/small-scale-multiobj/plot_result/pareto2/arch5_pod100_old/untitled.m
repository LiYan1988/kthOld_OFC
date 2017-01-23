clc;
close all;
clear;

result = zeros(22, 10, 20);
result0 = zeros(size(result));
r = zeros(22,20);
for i=0:19
    newFileName = sprintf('result_pareto_arch5_old_pod100_%d.csv',i);
    result(:,:,i+1) = importPareto(newFileName);
    result0(:,:,i+1) = result(:,:,i+1);
    r(:,1+i) = result(:,9,i+1)./result(:,3,i+1)./result(:,1,i+1);
    for j=1:22
        if r(j,i+1)<1
            result0(j,9,i+1) = result(j,9,i+1)./result(j,1,i+1);
        end
    end
end

