clc;
close all;
clear;

%% Load traffic matrices
connectionTotal = zeros(20, 1);
throughputTotal = zeros(20, 1);
for i = 1:20
    filename = sprintf('../trafficMatrices/traffic_matrix_pod250_load50_%d.csv', i-1);
    trafficMatrix = importTrafficMatrix(filename);
    connectionTotal(i) = sum(trafficMatrix(:)>0);
    throughputTotal(i) = sum(trafficMatrix(:));
end
connectionTotal = repmat(connectionTotal', 11, 1);
throughputTotal = repmat(throughputTotal', 11, 1);

%% Load results
corev = [];
connectionUb = zeros(11, 20);
throughputUb = zeros(11, 20);
objUb = zeros(11, 20);
connectionHeu = zeros(11, 20);
throughputHeu = zeros(11, 20);
objHeu = zeros(11, 20);

for i=1:20
    filename = sprintf('result_pareto_arch4_old_pod100_i%d.csv',i-1);
    [corev,connectionUb(:,i),throughputUb(:,i),objUb(:,i),~,...
        ~,~,connectionHeu(:,i),throughputHeu(:,i),objHeu(:,i)] = ...
        importResult(filename);
end

cnkUbA4G0 = 1-mean(connectionUb./connectionTotal, 2);
thpUbA4G0 = 1-mean(throughputUb./throughputTotal, 2);
objUbA4G0 = mean(objUb, 2);
cnkHeA4G0 = 1-mean(connectionHeu./connectionTotal, 2);
thpHeA4G0 = 1-mean(throughputHeu./throughputTotal, 2);
objHeA4G0 = mean(objHeu, 2);

%% Plot figures
% colors: [0, 0.45, 0.74], [.85, .33, .1], [.93, .69, .13]

figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(corev,thpUbA4G0, '--', ...
    'displayname', 'Optimal throughput', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(2) = plot(corev,thpHeA4G0, ...
    'displayname', 'Heuristic throughput', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]); % [.93, .69, .13]


figure2 = figure;
axes2 = axes('Parent', figure2);
box(axes2, 'on')
hold(axes2, 'on')
grid(axes2, 'on')
h(1) = plot(corev,cnkUbA4G0, '--', ...
    'displayname', 'Optimal connection', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(2) = plot(corev,cnkHeA4G0, ...
    'displayname', 'Heuristic connection', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]); % [.93, .69, .13]

save('arch4Guard0beta100.mat', 'cnkUbA4G0', 'thpUbA4G0', 'objUbA4G0', ...
    'cnkHeA4G0', 'thpHeA4G0', 'objHeA4G0')
