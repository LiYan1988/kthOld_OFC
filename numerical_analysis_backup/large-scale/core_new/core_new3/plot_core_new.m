clc;
clear;
close all;

cnk = zeros(20, 10);
blk = zeros(20, 10);
for i=1:20
    fn = sprintf('result_sa_core%d.csv', i-1);
    data = importfile(fn);
    tmp = zeros(20, 10);
    n = 1;
    for j=[1,2,3,5,6,7,9,10,11,13]
        tmp(:, n) = data{j};
        n = n+1;
    end
    for j=1:10
        cnk(i, j) = mean(tmp(:, j));
        blk(i, j) = mean((tmp(:, end)-tmp(:, j))./tmp(:, end));
    end
end

plot(blk(:,1:9),'DisplayName','blk(:,1:9)')
