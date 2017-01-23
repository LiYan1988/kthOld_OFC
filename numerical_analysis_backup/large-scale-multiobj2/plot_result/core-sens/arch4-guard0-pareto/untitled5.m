clc;
clear;
close all;

connection_ub=zeros(13, 20);
throughput_ub=zeros(13, 20);
obj_ub=zeros(13, 20);
connection_he=zeros(13, 20);
throughput_he=zeros(13, 20);
obj_he=zeros(13, 20);
for i=1:20
    fileName = sprintf('result_pareto_arch4_old_pod100_i%d.csv', i-1);
    [cores,connection_ub(:,i),throughput_ub(:,i),obj_ub(:,i),connection_lb,...
        throughput_lb,obj_lb,connection_he(:,i),throughput_he(:,i),obj_he(:,i)] = ...
        importResults(fileName);
end

figure; hold on;
plot(mean(connection_ub,2), mean(throughput_ub,2))
plot(mean(connection_he,2), mean(throughput_he,2))