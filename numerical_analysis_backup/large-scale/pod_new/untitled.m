clc;
clear;
close all;

blk = zeros(11, 10);
for i=1:11
    fn = sprintf('result_sa_core%d.csv',i-1);
    tmp = importfile(fn);
    for j=1:10
        blk(i, j) = mean((tmp(:,end)-tmp(:,j))./tmp(:,end));
    end
end