clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% 
%  PREFORMATTED
%  Optimality gaps are calculated differently for different architectues:
% 1. for architecture 2, the gap is between FF and lower bound
% 2. for architecture 4, it's between FF and the average of lower and upper
% bounds
% 3. for architecture 5, it's between FF and the upper bound
% 


% plot optimization gap for arch2 FF forward against connection
% optimization
arch2_FF_fwd_cnkgap_pod100 = 0.9509;
arch2_FF_fwd_thpgap_pod100 = 0.8585;

arch2_FF_fwd_cnkgap_pod150 = 0.9669;
arch2_FF_fwd_thpgap_pod150 = 0.8808;

arch2_FF_fwd_cnkgap_pod200 = 0.9914;
arch2_FF_fwd_thpgap_pod200 = 0.9373;

y = 1-[arch2_FF_fwd_cnkgap_pod100, arch2_FF_fwd_thpgap_pod100;...
    arch2_FF_fwd_cnkgap_pod150, arch2_FF_fwd_thpgap_pod150;...
    arch2_FF_fwd_cnkgap_pod200, arch2_FF_fwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 2 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.15], 4);
saveas(figure1, 'arch2_FF_ascending.jpg')

% plot optimization gap for arch2 FF backward against throughput
% optimization
arch2_FF_bwd_cnkgap_pod100 = 0.9865;
arch2_FF_bwd_thpgap_pod100 = 0.9559;

arch2_FF_bwd_cnkgap_pod150 = 0.9980;
arch2_FF_bwd_thpgap_pod150 = 0.9696;

arch2_FF_bwd_cnkgap_pod200 = 0.9941;
arch2_FF_bwd_thpgap_pod200 = 0.9751;

y = 1-fliplr([arch2_FF_bwd_cnkgap_pod100, arch2_FF_bwd_thpgap_pod100;...
    arch2_FF_bwd_cnkgap_pod150, arch2_FF_bwd_thpgap_pod150;...
    arch2_FF_bwd_cnkgap_pod200, arch2_FF_bwd_thpgap_pod200]);
title1 = 'Descending First Fit in Architecture 2 with Throughput Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.05], 6);
saveas(figure1, 'arch2_FF_descending.jpg')

% plot optimization gap for arch4 FF forward against connection
% optimization
arch4_FF_fwd_cnkgap_pod100 = 0.9712;
arch4_FF_fwd_thpgap_pod100 = 0.8784;

arch4_FF_fwd_cnkgap_pod150 = 0.9456;
arch4_FF_fwd_thpgap_pod150 = 0.9283;

arch4_FF_fwd_cnkgap_pod200 = 0.9657;
arch4_FF_fwd_thpgap_pod200 = 0.9368;

y = 1-[arch4_FF_fwd_cnkgap_pod100, arch4_FF_fwd_thpgap_pod100;...
    arch4_FF_fwd_cnkgap_pod150, arch4_FF_fwd_thpgap_pod150;...
    arch4_FF_fwd_cnkgap_pod200, arch4_FF_fwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 4 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.15], 4);
saveas(figure1, 'arch4_FF_ascending.jpg')

% plot optimization gap for arch4 FF backward against throughput
% optimization
arch4_FF_bwd_cnkgap_pod100 = 0.9703;
arch4_FF_bwd_thpgap_pod100 = 0.9657;

arch4_FF_bwd_cnkgap_pod150 = 0.9839;
arch4_FF_bwd_thpgap_pod150 = 0.9672;

arch4_FF_bwd_cnkgap_pod200 = 0.9945;
arch4_FF_bwd_thpgap_pod200 = 0.9664;

y = 1-fliplr([arch4_FF_bwd_cnkgap_pod100, arch4_FF_bwd_thpgap_pod100;...
    arch4_FF_bwd_cnkgap_pod150, arch4_FF_bwd_thpgap_pod150;...
    arch4_FF_bwd_cnkgap_pod200, arch4_FF_bwd_thpgap_pod200]);
title1 = 'Descending First Fit in Architecture 4 with Throughput Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.04], 5);
saveas(figure1, 'arch4_FF_descending.jpg')

% plot optimization gap for arch5 FF forward against connection
% optimization
arch5_FF_fwd_cnkgap_pod100 = 0.8917;
arch5_FF_fwd_thpgap_pod100 = 0.7610;

arch5_FF_fwd_cnkgap_pod150 = 0.8969;
arch5_FF_fwd_thpgap_pod150 = 0.7484;

arch5_FF_fwd_cnkgap_pod200 = 0.8991;
arch5_FF_fwd_thpgap_pod200 = 0.7636;

y = 1-[arch5_FF_fwd_cnkgap_pod100, arch5_FF_fwd_thpgap_pod100;...
    arch5_FF_fwd_cnkgap_pod150, arch5_FF_fwd_thpgap_pod150;...
    arch5_FF_fwd_cnkgap_pod200, arch5_FF_fwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 5 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [0, 0.30], 4);
saveas(figure1, 'arch5_FF_ascending.jpg')

% plot optimization gap for arch5 FF backward against throughput
% optimization
arch5_FF_bwd_cnkgap_pod100 = 1.2457;
arch5_FF_bwd_thpgap_pod100 = 0.9286;

arch5_FF_bwd_cnkgap_pod150 = 1.4178;
arch5_FF_bwd_thpgap_pod150 = 0.9636;

arch5_FF_bwd_cnkgap_pod200 = 1.4920;
arch5_FF_bwd_thpgap_pod200 = 0.9755;

y = 1-[arch5_FF_bwd_cnkgap_pod100, arch5_FF_bwd_thpgap_pod100;...
    arch5_FF_bwd_cnkgap_pod150, arch5_FF_bwd_thpgap_pod150;...
    arch5_FF_bwd_cnkgap_pod200, arch5_FF_bwd_thpgap_pod200];
title1 = 'Descending First Fit in Architecture 5 with Throughput Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';
figure1 = createfigure_optimality_gap(y, title1, xlabel1, ylabel1, [-0.50, 0.1], 5, 'SouthWest');
saveas(figure1, 'arch5_FF_descending.jpg')
% the connection optimality gaps are negative because the difference
% between connection capacities are too large, so the resources are highly
% fregmented. The FF descending algorithm fills these holes with small
% connections. If we make the distribution of connection capacity more
% uniform, the connection optimality gaps should be less negative.