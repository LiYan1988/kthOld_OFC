clc;
clear;
close all;

data_ave = zeros(20,7);
cnk_ave = zeros(20,7);
for i=0:19
    fn = sprintf('result_sa_core%d.csv',i);
    dataArray = importfile(fn);
    for j=1:6
        data_ave(i+1,j) = mean((dataArray{7}-dataArray{j})./dataArray{7});
        cnk_ave(i+1,j) = mean(dataArray{j});
    end
    data_ave(i+1,7) = mean(dataArray{7});
    cnk_ave(i+1,7) = mean(dataArray{7});
end
