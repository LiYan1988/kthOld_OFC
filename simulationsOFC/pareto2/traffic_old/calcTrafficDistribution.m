clc;
clear;
close all;

Nmatrices = 20;
edges = [1, 10, 100, 200, 400, 1000, 2000];
trafficMatrix = cell(Nmatrices, 1);
binCounts = zeros(Nmatrices, 6);
binIndices = cell(Nmatrices, 1);
for i=1:20
    filename = sprintf('traffic_matrix_old_%d.csv', i-1);
    trafficMatrix{i} = importTrafficMatrix(filename);
    [binCounts(i, :), binIndices{i}] = histcounts(trafficMatrix{i}(:), edges);
end
binN = mean(binCounts);
binN = binN/sum(binN);
binT = mean(binCounts)'.*[1; 10; 100; 200; 400; 1000];
binT = binT/sum(binT);