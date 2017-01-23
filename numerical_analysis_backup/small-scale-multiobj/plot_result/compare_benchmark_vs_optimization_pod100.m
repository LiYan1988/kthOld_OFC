% POD 100, arch2, compare optimization gap between FF forward, FF backward,
% Ajmal, and optimizations

clc;
clear;
close all;

%% Import data
% import benchmark data
fileName1 = 'pod100_benchmark.csv';
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
fileName1 = 'pod100_connections.csv';
[id,arch4_cnkopt_lb_cnk,arch4_cnkopt_ub_cnk,...
    arch4_cnkopt_lb_thp,arch4_cnkopt_ub_thp,...
    arch1_cnkopt_cnk,arch1_cnkopt_thp,...
    arch2_cnkopt_lb_cnk,arch2_cnkopt_ub_cnk,...
    arch2_cnkopt_lb_thp,arch2_cnkopt_ub_thp,...
    arch5_cnkopt_lb_cnk,arch5_cnkopt_ub_cnk,...
    arch5_cnkopt_lb_thp,arch5_cnkopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% throughput
fileName1 = 'pod100_throughput.csv';
[id,arch4_thpopt_lb_cnk,arch4_thpopt_ub_cnk,...
    arch4_thpopt_lb_thp,arch4_thpopt_ub_thp,...
    arch1_thpopt_cnk,arch1_thpopt_thp,...
    arch2_thpopt_lb_cnk,arch2_thpopt_ub_cnk,...
    arch2_thpopt_lb_thp,arch2_thpopt_ub_thp,...
    arch5_thpopt_lb_cnk,arch5_thpopt_ub_cnk,...
    arch5_thpopt_lb_thp,arch5_thpopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% hybrid
fileName1 = 'pod100_hybrid.csv';
[id,arch4_hybopt_lb_cnk,arch4_hybopt_ub_cnk,...
    arch4_hybopt_lb_thp,arch4_hybopt_ub_thp,...
    arch1_hybopt_cnk,arch1_hybopt_thp,...
    arch2_hybopt_lb_cnk,arch2_hybopt_ub_cnk,...
    arch2_hybopt_lb_thp,arch2_hybopt_ub_thp,...
    arch5_hybopt_lb_cnk,arch5_hybopt_ub_cnk,...
    arch5_hybopt_lb_thp,arch5_hybopt_ub_thp,total_cnk] = ...
    importfile_optimizations_vectors(fileName1);

% SAfileName1 = 'pod100_arch2_sa.csv';
% [hybridCNK,hybridTRP,...
%     connectionsCNK,connectionsTRP,...
%     throughputCNK,throughputTRP] = importfile_sa_vectors(fileName1);

%% Compare FF forward with optimization on connections and throughput
% arch 2 cnk
arch2_FF_fwd_cnkgap_lb = Arch2_FF_fwd_cnk./arch2_cnkopt_lb_cnk;
arch2_FF_fwd_cnkgap_ub = Arch2_FF_fwd_cnk./arch2_cnkopt_ub_cnk;
% arch 2 thp
arch2_FF_fwd_thpgap_lb = Arch2_FF_fwd_thp./arch2_cnkopt_lb_thp;
arch2_FF_fwd_thpgap_ub = Arch2_FF_fwd_thp./arch2_cnkopt_ub_thp;
% AFF CNK LB
% mean(arch2_FF_fwd_cnkgap_lb) % 95.09%
% mean(arch2_FF_fwd_thpgap_lb) % 85.85%
% AFF CNK UB
% mean(arch2_FF_fwd_cnkgap_ub) % 88.18%
% mean(arch2_FF_fwd_thpgap_ub) % 73.94%
% AFF 
% mean(Arch2_FF_fwd_cnk) % 
% mean(Arch2_FF_fwd_thp) % 
% % OPT 
% mean(arch2_cnkopt_lb_cnk) % 
% mean(arch2_cnkopt_lb_thp) % 
% 
% 
% 1.146450000000000e+03
% 183400
% 1.205600000000000e+03
% 2.136387500000000e+05


% arch 4
arch4_FF_fwd_cnkgap_lb = Arch4_FF_fwd_cnk./arch4_cnkopt_lb_cnk;
arch4_FF_fwd_cnkgap_ub = Arch4_FF_fwd_cnk./arch4_cnkopt_ub_cnk;
arch4_FF_fwd_thpgap_lb = Arch4_FF_fwd_thp./arch4_cnkopt_lb_thp;
arch4_FF_fwd_thpgap_ub = Arch4_FF_fwd_thp./arch4_cnkopt_ub_thp;
% AFF CNK LB
% mean(arch4_FF_fwd_cnkgap_lb) % 97.12%
% mean(arch4_FF_fwd_thpgap_lb) % 87.84%
% AFF CNK UB
% mean(arch4_FF_fwd_thpgap_ub) % 68.46%
% mean(arch4_FF_fwd_cnkgap_ub) % 87.07%
% mean(Arch4_FF_fwd_cnk) 
% mean(Arch4_FF_fwd_thp) 
% mean(arch4_cnkopt_lb_cnk) 
% mean(arch4_cnkopt_lb_thp) 
% 
% 9.261000000000000e+02
% 111870
% 9.535000000000000e+02
% 1.274275000000000e+05

% arch 5
% arch5_FF_fwd_cnkgap_lb = Arch5_FF_fwd_cnk./arch5_cnkopt_lb_cnk;
arch5_FF_fwd_cnkgap_ub = Arch5_FF_fwd_cnk./arch5_cnkopt_ub_cnk;
% mean(arch5_FF_fwd_cnkgap_lb) % 178.41%, lower bounds are wrong
% mean(arch5_FF_fwd_cnkgap_ub) % 89.17%
arch5_FF_fwd_thpgap_ub = Arch5_FF_fwd_thp./arch5_cnkopt_ub_thp;
% mean(arch5_FF_fwd_thpgap_ub) % 76.10%

% mean(Arch5_FF_fwd_cnk) 
% mean(Arch5_FF_fwd_thp) 
% mean(arch5_cnkopt_ub_cnk) 
% mean(arch5_cnkopt_ub_thp) 
% 
% 1.159450000000000e+03
% 188820
% 1.300300000000000e+03
% 2.481237500000000e+05

% Optimal gap on connections:
% arch2: 88.18%; arch4: 87.97%; arch5 89.17%

% mean(arch5_cnkopt_ub_cnk./arch2_cnkopt_ub_cnk) % 100%
% mean(arch5_cnkopt_ub_cnk./arch2_cnkopt_lb_cnk) % 107%
% mean(arch5_cnkopt_ub_thp./arch2_cnkopt_ub_thp) % 100.03%
% mean(arch5_cnkopt_ub_thp./arch2_cnkopt_lb_thp) % 116.15%

% Conclusion: 
% 1. The upper bound optimal gap of FF forward on connections is around 12%
% 2. The difference between upper bounds of arch2 and 5 is 0%
% 3. The upper bound optimal gap of FF forward on throughput is around 30%
% TO-DO:
% 1. Reduce problem size so that arch2 can be solved optimally, then
% compare with arch5

%% Compare FF backward with optimization on connections and throughput
% arch 2 cnk
arch2_FF_bwd_cnkgap_lb = Arch2_FF_bwd_cnk./arch2_thpopt_lb_cnk;
arch2_FF_bwd_cnkgap_ub = Arch2_FF_bwd_cnk./arch2_thpopt_ub_cnk;
% arch 2 thp
arch2_FF_bwd_thpgap_lb = Arch2_FF_bwd_thp./arch2_thpopt_lb_thp;
arch2_FF_bwd_thpgap_ub = Arch2_FF_bwd_thp./arch2_thpopt_ub_thp;
% DFF THR LB
% mean(arch2_FF_bwd_cnkgap_lb) % 98.65%
% mean(arch2_FF_bwd_thpgap_lb) % 95.59%
% DFF THR UB
% mean(arch2_FF_bwd_cnkgap_ub) % 93.33%
% mean(arch2_FF_bwd_thpgap_ub) % 92.78%

% mean(Arch2_FF_bwd_cnk)
% mean(Arch2_FF_bwd_thp)
% mean(arch2_thpopt_lb_cnk)
% mean(arch2_thpopt_lb_thp)
% 
% 6.177500000000000e+02
% 2.603487500000000e+05
% 6.263000000000000e+02
% 2.723775000000000e+05

% arch 4
arch4_FF_bwd_cnkgap_lb = Arch4_FF_bwd_cnk./arch4_thpopt_lb_cnk;
arch4_FF_bwd_cnkgap_ub = Arch4_FF_bwd_cnk./arch4_thpopt_ub_cnk;
arch4_FF_bwd_thpgap_lb = Arch4_FF_bwd_thp./arch4_thpopt_lb_thp;
arch4_FF_bwd_thpgap_ub = Arch4_FF_bwd_thp./arch4_thpopt_ub_thp;
% DFF THR LB
% mean(arch4_FF_bwd_cnkgap_lb) % 101.35%
% mean(arch4_FF_bwd_thpgap_lb) % 101.97%
% DFF THR UB
% mean(arch4_FF_bwd_cnkgap_ub) % 92.70%
% mean(arch4_FF_bwd_thpgap_ub) % 91.78%

% mean(Arch4_FF_bwd_cnk)
% mean(Arch4_FF_bwd_thp)
% mean(arch4_thpopt_lb_cnk)
% mean(arch4_thpopt_lb_thp)
% 
% 
% 3.474500000000000e+02
% 2.309675000000000e+05
% 3.429500000000000e+02
% 2.265687500000000e+05

% arch 5
arch5_FF_bwd_cnkgap_ub = Arch5_FF_bwd_cnk./arch5_thpopt_ub_cnk;
arch5_FF_bwd_thpgap_ub = Arch5_FF_bwd_thp./arch5_thpopt_ub_thp;
% mean(arch5_FF_bwd_cnkgap_ub) % 124.57%
% mean(arch5_FF_bwd_thpgap_ub) % 92.86%

mean(Arch5_FF_bwd_cnk)
mean(Arch5_FF_bwd_thp)
mean(arch5_thpopt_ub_cnk)
mean(arch5_thpopt_ub_thp)



% Optimal gap on throughput:
% arch2: 92.78%; arch4: 91.78%; arch5 92.86%

% mean(arch5_thpopt_ub_cnk./arch2_thpopt_ub_cnk) % 75.08%
% mean(arch5_thpopt_ub_cnk./arch2_thpopt_lb_cnk) % 79.37%
% mean(arch5_thpopt_ub_thp./arch2_thpopt_ub_thp) % 100.00%
% mean(arch5_thpopt_ub_thp./arch2_thpopt_lb_thp) % 103.02%

% Conclusion: 
% 1. The upper bound optimal gap of FF backward on throughput is around 8%
% 2. The difference between arch2 and 5 in throughput upper bound is 0%
% 3. The upper bound optimal gap of FF backward on connection is around 7%
% 4. In arch 5, FF backward allocates more connections, but less throughput
% TO-DO:
% 1. solve arch 2 and 5 optimally in small size problems

%% Compare Ajmal's algorithm with optimizations on connections and throughput
% connection
arch2_AJ_bwd_cnk_lb = Arch2_AJ_bwd_cnk./arch2_cnkopt_lb_cnk;
arch2_AJ_bwd_cnk_ub = Arch2_AJ_bwd_cnk./arch2_cnkopt_ub_cnk;
% mean(arch2_AJ_bwd_cnk_lb) % 80.41%
% mean(arch2_AJ_bwd_cnk_ub) % 74.56%
% throughput
arch2_AJ_bwd_thp_lb = Arch2_AJ_bwd_thp./arch2_cnkopt_lb_thp;
arch2_AJ_bwd_thp_ub = Arch2_AJ_bwd_thp./arch2_cnkopt_ub_thp;
% mean(arch2_AJ_bwd_thp_lb) % 109.65%
% mean(arch2_AJ_bwd_thp_ub) % 94.44%

% connection
arch4_AJ_bwd_cnk_lb = Arch4_AJ_bwd_cnk./arch4_cnkopt_lb_cnk;
arch4_AJ_bwd_cnk_ub = Arch4_AJ_bwd_cnk./arch4_cnkopt_ub_cnk;
% mean(arch4_AJ_bwd_cnk_lb) % 43.88%
% mean(arch4_AJ_bwd_cnk_ub) % 39.34%
% throughput
arch4_AJ_bwd_thp_lb = Arch4_AJ_bwd_thp./arch4_cnkopt_lb_thp;
arch4_AJ_bwd_thp_ub = Arch4_AJ_bwd_thp./arch4_cnkopt_ub_thp;
% mean(arch4_AJ_bwd_thp_lb) % 176.60%
% mean(arch4_AJ_bwd_thp_ub) % 137.61%

% connection
arch5_AJ_bwd_cnk_ub = Arch5_AJ_bwd_cnk./arch5_cnkopt_ub_cnk;
% mean(arch5_AJ_bwd_cnk_ub) % 74.60%
% throughput
arch5_AJ_bwd_thp_ub = Arch5_AJ_bwd_thp./arch5_cnkopt_ub_thp;
% mean(arch5_AJ_bwd_thp_ub) % 94.63%

% Conclusion: 
% 1. Ajmal's algorithm is originally for saving reosurce in meshed network,
% so it doesn't perform well in connection number maximization.
% 2. The algorithm somehow achieves a balance between the connection and
% throughput maximizations, as seen from the large connection optimality 
% gaps and the small or even negative throughput optimality gaps.
% TO-DO:
% What is the best algorithm to achieve the trade-off between the two
% objectives?