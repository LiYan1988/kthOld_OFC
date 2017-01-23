clc;
clear;
close all;

blk_log = zeros(14, 10);
for i=12:27
    fn = sprintf('result_sa_core%d.csv',i);
    tmp = importfile(fn);
    for j=1:10
        blk_log(i, j) = mean((tmp(:,end)-tmp(:,j))./tmp(:,end));
    end
end