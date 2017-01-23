clc;
clear;
close all;

data_ave = zeros(20,10);
cnk_ave = zeros(20,10);

for i=0:19
    fn = sprintf('result_sa_core%d.csv',i);
    try
        dataArray = importfile(fn);
        for j=1:9
            data_ave(i+1,j) = mean((dataArray{10}-dataArray{j})./dataArray{10});
            cnk_ave(i+1,j) = mean(dataArray{j});
        end
        data_ave(i+1,10) = mean(dataArray{10});
        cnk_ave(i+1,10) = mean(dataArray{10});
    catch
        
    end
end

figure(1);
plot(data_ave(:,1:3))
figure(2);
plot(data_ave(:,4:6))
figure(3);
plot(data_ave(:,7:9))

save('data_load_ave.mat','data_ave')