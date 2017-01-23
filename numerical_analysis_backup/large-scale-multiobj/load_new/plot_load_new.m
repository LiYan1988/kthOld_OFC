% clc;
% clear;
% close all;

blk = zeros(19, 10);
for i=1:19
    fn = sprintf('result_sa_core%d.csv',i-1);
    tmp = importfile1(fn);
    cidx = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13];
    for j=1:10
        blk(i, j) = mean((tmp(:, end)-tmp(:, cidx(j)))./tmp(:, end));
    end
end

figure(); box on; grid on;
plot(blk(:,1:9),'DisplayName','blk(:,1:9)')
