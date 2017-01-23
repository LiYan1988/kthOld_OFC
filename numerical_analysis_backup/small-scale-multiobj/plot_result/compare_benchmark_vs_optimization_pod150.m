% POD 100, arch2, compare optimization gap between FF forward, FF backward,
% Ajmal, and optimizations

clc;
clear;
close all;

%% Import data
% import benchmark data
fileName1 = 'pod150_benchmark.csv';
[Arch2_FF_fwd_cnk,Arch2_FF_fwd_thp,...
 Arch2_FF_bwd_cnk,Arch2_FF_bwd_thp,...
 Arch2_AJ_fwd_cnk,Arch2_AJ_fwd_thp,...
 Arch2_AJ_bwd_cnk,Arch2_AJ_bwd_thp,...
 Arch4_FF_fwd_cnk,Arch4_FF_fwd_thp,...
 Arch4_FF_bwd_cnk,Arch4_FF_bwd_thp,...
 Arch4_AJ_fwd_cnk,Arch4_AJ_fwd_thp,...
 Arch4_AJ_bwd_cnk,Arch4_AJ_bwd_thp,...
 Arch5_FF_fwd_cnk,Arch5_FF_fwd_thp,...
 Arch5_FF_bwd_cnk,Arch5_FF_bwd_thp,...
 Arch5_AJ_fwd_cnk,Arch5_AJ_fwd_thp,...
 Arch5_AJ_bwd_cnk,Arch5_AJ_bwd_thp] = ...
 importfile_benchmark_vectors(fileName1);

% import MILP data
% connections
fileName1 = 'pod150_connections.csv';
[id,arch4_cnkopt_lb_cnk,arch4_cnkopt_ub_cnk,...
    arch4_cnkopt_lb_thp,arch4_cnkopt_ub_thp,...
    arch1_cnkopt_cnk,arch1_cnkopt_thp,...
    arch2_cnkopt_lb_cnk,arch2_cnkopt_ub_cnk,...
    arch2_cnkopt_lb_thp,arch2_cnkopt_ub_thp,...
    arch5_cnkopt_lb_cnk,arch5_cnkopt_ub_cnk,...
    arch5_cnkopt_lb_thp,arch5_cnkopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% throughput
fileName1 = 'pod150_throughput.csv';
[id,arch4_thpopt_lb_cnk,arch4_thpopt_ub_cnk,...
    arch4_thpopt_lb_thp,arch4_thpopt_ub_thp,...
    arch1_thpopt_cnk,arch1_thpopt_thp,...
    arch2_thpopt_lb_cnk,arch2_thpopt_ub_cnk,...
    arch2_thpopt_lb_thp,arch2_thpopt_ub_thp,...
    arch5_thpopt_lb_cnk,arch5_thpopt_ub_cnk,...
    arch5_thpopt_lb_thp,arch5_thpopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% hybrid
fileName1 = 'pod150_hybrid.csv';
[id,arch4_hybopt_lb_cnk,arch4_hybopt_ub_cnk,...
    arch4_hybopt_lb_thp,arch4_hybopt_ub_thp,...
    arch1_hybopt_cnk,arch1_hybopt_thp,...
    arch2_hybopt_lb_cnk,arch2_hybopt_ub_cnk,...
    arch2_hybopt_lb_thp,arch2_hybopt_ub_thp,...
    arch5_hybopt_lb_cnk,arch5_hybopt_ub_cnk,...
    arch5_hybopt_lb_thp,arch5_hybopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% SAfileName1 = 'pod100_arch2_sa.csv';
pod100Sa = importfile_sa(fileName1);
[hybridCNK,hybridTRP,...
    connectionsCNK,connectionsTRP,...
    throughputCNK,throughputTRP] = importfile_sa_vectors(fileName1);

%% Compare FF forward with optimization on connections and throughput
% arch 2 cnk
arch2_FF_fwd_cnkgap_lb = Arch2_FF_fwd_cnk./arch2_cnkopt_lb_cnk;
arch2_FF_fwd_cnkgap_ub = Arch2_FF_fwd_cnk./arch2_cnkopt_ub_cnk;
% mean(arch2_FF_fwd_cnkgap_lb) % 96.69%
% mean(arch2_FF_fwd_cnkgap_ub) % 88.82%
% arch 2 thp
arch2_FF_fwd_thpgap_lb = Arch2_FF_fwd_thp./arch2_cnkopt_lb_thp;
arch2_FF_fwd_thpgap_ub = Arch2_FF_fwd_thp./arch2_cnkopt_ub_thp;
% mean(arch2_FF_fwd_thpgap_lb) % 88.08%
% mean(arch2_FF_fwd_thpgap_ub) % 72.92%
% arch2_FF_fwd_cnkgap_pod150 = 0.9669;
% arch2_FF_fwd_thpgap_pod150 = 0.8808;
 
% mean(Arch2_FF_fwd_cnk) % 2222.65
% mean(Arch2_FF_fwd_thp) % 271987.5
% mean(arch2_cnkopt_lb_cnk) % 2298.7
% mean(arch2_cnkopt_lb_thp) % 308841.3

% arch 4
arch4_FF_fwd_cnkgap_lb = Arch4_FF_fwd_cnk./arch4_cnkopt_lb_cnk;
arch4_FF_fwd_cnkgap_ub = Arch4_FF_fwd_cnk./arch4_cnkopt_ub_cnk;
% mean(arch4_FF_fwd_cnkgap_lb) % 101.69%
% mean(arch4_FF_fwd_cnkgap_ub) % 87.43%
arch4_FF_fwd_thpgap_lb = Arch4_FF_fwd_thp./arch4_cnkopt_lb_thp;
arch4_FF_fwd_thpgap_ub = Arch4_FF_fwd_thp./arch4_cnkopt_ub_thp;
% mean(arch4_FF_fwd_thpgap_lb) % 92.83%
% mean(arch4_FF_fwd_thpgap_ub) % 69.06%


% mean(Arch4_FF_fwd_cnk) % 1675.4
% mean(Arch4_FF_fwd_thp) % 146472.5
% mean(arch4_cnkopt_lb_cnk) % 1647.7
% mean(arch4_cnkopt_lb_thp) % 157817.5

% arch 5
arch5_FF_fwd_cnkgap_ub = Arch5_FF_fwd_cnk./arch5_cnkopt_ub_cnk;
% mean(arch5_FF_fwd_cnkgap_ub) % 89.69%
arch5_FF_fwd_thpgap_ub = Arch5_FF_fwd_thp./arch5_cnkopt_ub_thp;
% mean(arch5_FF_fwd_thpgap_ub) % 74.84%

% mean(Arch5_FF_fwd_cnk) % 2244.6
% mean(Arch5_FF_fwd_thp) % 279237.5
% mean(arch5_cnkopt_ub_cnk) % 2502.5
% mean(arch5_cnkopt_ub_thp) % 373092.5

% Optimal gap on connections:
% arch2: 88.82%; arch4: 87.43%; arch5 89.69%

% mean(arch5_cnkopt_ub_cnk./arch2_cnkopt_ub_cnk) % 100.01%
% mean(arch5_cnkopt_ub_cnk./arch2_cnkopt_lb_cnk) % 108.87%
% mean(arch5_cnkopt_ub_thp./arch2_cnkopt_ub_thp) % 100.02%
% mean(arch5_cnkopt_ub_thp./arch2_cnkopt_lb_thp) % 120.82%

% Conclusion: same as POD 100
% 1. The upper bound optimal gap of FF forward on connections is around 12%
% 2. The difference between connection upper bounds of arch2 and 5 is 0%
% 3. The upper bound optimal gap of FF forward on throughput is around 30%

%% compare FF backward with optimization on connections and throughput
% arch 2 cnk
arch2_FF_bwd_cnkgap_lb = Arch2_FF_bwd_cnk./arch2_thpopt_lb_cnk;
arch2_FF_bwd_cnkgap_ub = Arch2_FF_bwd_cnk./arch2_thpopt_ub_cnk;
% mean(arch2_FF_bwd_cnkgap_lb) % 99.80%
% mean(arch2_FF_bwd_cnkgap_ub) % 97.21%
% arch 2 thp
arch2_FF_bwd_thpgap_lb = Arch2_FF_bwd_thp./arch2_thpopt_lb_thp;
arch2_FF_bwd_thpgap_ub = Arch2_FF_bwd_thp./arch2_thpopt_ub_thp;
% mean(arch2_FF_bwd_thpgap_lb) % 96.96%
% mean(arch2_FF_bwd_thpgap_ub) % 95.52%


% mean(Arch2_FF_bwd_cnk)
% mean(Arch2_FF_bwd_thp)
% mean(arch2_thpopt_lb_cnk)
% mean(arch2_thpopt_lb_thp)
% 
% 9.163000000000000e+02
% 405475
% 9.183000000000000e+02
% 4.181762500000000e+05

% arch 4
arch4_FF_bwd_cnkgap_lb = Arch4_FF_bwd_cnk./arch4_thpopt_lb_cnk;
arch4_FF_bwd_cnkgap_ub = Arch4_FF_bwd_cnk./arch4_thpopt_ub_cnk;
% mean(arch4_FF_bwd_cnkgap_lb) % 105.29%
% mean(arch4_FF_bwd_cnkgap_ub) % 99.39%
arch4_FF_bwd_thpgap_lb = Arch4_FF_bwd_thp./arch4_thpopt_lb_thp;
arch4_FF_bwd_thpgap_ub = Arch4_FF_bwd_thp./arch4_thpopt_ub_thp;
% mean(arch4_FF_bwd_thpgap_lb) % 99.35%
% mean(arch4_FF_bwd_thpgap_ub) % 94.08%

% mean(Arch4_FF_bwd_cnk)
% mean(Arch4_FF_bwd_thp)
% mean(arch4_thpopt_lb_cnk)
% mean(arch4_thpopt_lb_thp)
% 
% 4.896500000000000e+02
% 3.625762500000000e+05
% 4.651000000000000e+02
% 3.650162500000000e+05


% arch 5
arch5_FF_bwd_cnkgap_ub = Arch5_FF_bwd_cnk./arch5_thpopt_ub_cnk;
% mean(arch5_FF_bwd_cnkgap_ub) % 141.78%
arch5_FF_bwd_thpgap_ub = Arch5_FF_bwd_thp./arch5_thpopt_ub_thp;
% mean(arch5_FF_bwd_thpgap_ub) % 96.36%

% mean(Arch5_FF_bwd_cnk)
% mean(Arch5_FF_bwd_thp)
% mean(arch5_thpopt_ub_cnk)
% mean(arch5_thpopt_ub_thp)
% 
% 9.169500000000000e+02
% 405680
% 6.477000000000000e+02
% 4.210037500000000e+05

% Optimal gap on throughput:
% arch2: 95.52%; arch4: 914.08%; arch5 96.36%

% mean(arch5_thpopt_ub_cnk./arch2_thpopt_ub_cnk) % 68.70%
% mean(arch5_thpopt_ub_cnk./arch2_thpopt_lb_cnk) % 70.54%
% mean(arch5_thpopt_ub_thp./arch2_thpopt_ub_thp) % 99.18%
% mean(arch5_thpopt_ub_thp./arch2_thpopt_lb_thp) % 100.68%

% Conclusion: 
% 1. throughput upper bound gap is around 5%
% 2. connection upper bound gap is around less than 4%

%% Compare Ajmal's algorithm with optimizations on connections and throughput
% connection
arch2_AJ_bwd_cnk_lb = Arch2_AJ_bwd_cnk./arch2_cnkopt_lb_cnk;
arch2_AJ_bwd_cnk_ub = Arch2_AJ_bwd_cnk./arch2_cnkopt_ub_cnk;
% mean(arch2_AJ_bwd_cnk_lb) % 66.79%
% mean(arch2_AJ_bwd_cnk_ub) % 61.35%
% throughput
arch2_AJ_bwd_thp_lb = Arch2_AJ_bwd_thp./arch2_cnkopt_lb_thp;
arch2_AJ_bwd_thp_ub = Arch2_AJ_bwd_thp./arch2_cnkopt_ub_thp;
% mean(arch2_AJ_bwd_thp_lb) % 122.73%
% mean(arch2_AJ_bwd_thp_ub) % 101.61%

% connection
arch4_AJ_bwd_cnk_lb = Arch4_AJ_bwd_cnk./arch4_cnkopt_lb_cnk;
arch4_AJ_bwd_cnk_ub = Arch4_AJ_bwd_cnk./arch4_cnkopt_ub_cnk;
% mean(arch4_AJ_bwd_cnk_lb) % 37.39%
% mean(arch4_AJ_bwd_cnk_ub) % 32.15%
% throughput
arch4_AJ_bwd_thp_lb = Arch4_AJ_bwd_thp./arch4_cnkopt_lb_thp;
arch4_AJ_bwd_thp_ub = Arch4_AJ_bwd_thp./arch4_cnkopt_ub_thp;
% mean(arch4_AJ_bwd_thp_lb) % 222.66%
% mean(arch4_AJ_bwd_thp_ub) % 165.67%

% connection
arch5_AJ_bwd_cnk_ub = Arch5_AJ_bwd_cnk./arch5_cnkopt_ub_cnk;
% mean(arch5_AJ_bwd_cnk_ub) % 61.35%
% throughput
arch5_AJ_bwd_thp_ub = Arch5_AJ_bwd_thp./arch5_cnkopt_ub_thp;
% mean(arch5_AJ_bwd_thp_ub) % 101.63%
