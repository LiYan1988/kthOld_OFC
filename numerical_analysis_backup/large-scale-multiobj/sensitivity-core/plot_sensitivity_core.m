clc;
clear;
close all;

data_ave = zeros(20,10);
cnk_ave = zeros(20,10);
for i=0:19
    fn = sprintf('result_sa_core%d.csv',i);
    dataArray = importfile(fn);
    for j=1:9
        data_ave(i+1,j) = mean((dataArray{10}-dataArray{j})./dataArray{10});
        cnk_ave(i+1,j) = mean(dataArray{j});
    end
    data_ave(i+1,10) = mean(dataArray{10});
    cnk_ave(i+1,10) = mean(dataArray{10});
end
plot(data_ave(:,1:9))

for i=[1,2,3,7,8,9]
    cnk_ave(:,i) = smooth(cnk_ave(:,i),3);
end
figure(1);
plot(cnk_ave(:,1:3))
figure(2);
plot(cnk_ave(:,4:6))
figure(3);
plot(cnk_ave(:,7:9))

save('data_ave.mat','cnk_ave')