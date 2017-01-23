clc;
clear;
close all;

%% Load traffic matrices
connectionTotal = zeros(20, 1);
throughputTotal = zeros(20, 1);
for i = 1:20
    filename = sprintf('../trafficMatrices/traffic_matrix_pod250_load50_%d.csv', i-1);
    trafficMatrix = importTrafficMatrix(filename);
    connectionTotal(i) = sum(trafficMatrix(:)>0);
    throughputTotal(i) = sum(trafficMatrix(:));
end
connectionTotal = repmat(connectionTotal', 8, 1);
throughputTotal = repmat(throughputTotal', 8, 1);

%% 
cores = zeros(8, 1);
cnkub = zeros(8, 20);
thpub = zeros(8, 20);
objub = zeros(8, 20);
for i=1:4
    for j=1:20
        fileName = sprintf('result_pareto_arch5_old_%d_%d.csv', i, j-1);
        cv = ((i-1)*2+1):(i*2);
        [cores(cv), cnkub(cv, j), thpub(cv, j), objub(cv, j)] = ...
            importResults(fileName);
    end
end

cnkUbA5G1 = 1-mean(cnkub./connectionTotal, 2);
thpUbA5G1 = 1-mean(thpub./throughputTotal, 2);
objUbA5G1 = mean(objub, 2);

plot(cores, cnkUbA5G1)
figure; 
plot(cores, thpUbA5G1)

save('arch5Guard1beta0.mat', ...
    'cnkUbA5G1', 'thpUbA5G1', 'objUbA5G1')