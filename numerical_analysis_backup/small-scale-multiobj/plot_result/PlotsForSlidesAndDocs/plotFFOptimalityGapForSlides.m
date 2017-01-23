clc;
close all;
clear;
% optimality gaps of FF ascending and descending for different architecture
% and number of PODs

%%
% % plot optimization gap for arch2 FF forward against connection
% % optimization
% arch2_FF_fwd_cnkgap_pod100 = 0.9509;
% arch2_FF_fwd_cnkgap_pod150 = 0.9669;
% arch2_FF_fwd_cnkgap_pod200 = 0.9914;
% 
% arch4_FF_fwd_cnkgap_pod100 = 0.9712;
% arch4_FF_fwd_cnkgap_pod150 = 0.9456;
% arch4_FF_fwd_cnkgap_pod200 = 0.9657;
% 
% arch5_FF_fwd_cnkgap_pod100 = 0.8917;
% arch5_FF_fwd_cnkgap_pod150 = 0.8969;
% arch5_FF_fwd_cnkgap_pod200 = 0.8991;
% 
% y = 1-...
%     [arch2_FF_fwd_cnkgap_pod100, arch4_FF_fwd_cnkgap_pod100, arch5_FF_fwd_cnkgap_pod100;...
%     arch2_FF_fwd_cnkgap_pod150, arch4_FF_fwd_cnkgap_pod150, arch5_FF_fwd_cnkgap_pod150;...
%     arch2_FF_fwd_cnkgap_pod200, arch4_FF_fwd_cnkgap_pod200, arch5_FF_fwd_cnkgap_pod200];
% title1 = 'Ascending First Fit in Architecture 2 with Connection Optimized';
% xlabel1 = 'Number of PODs';
% ylabel1 = 'Optimality gap';
% 
% figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
% 
% % Create axes
% axes1 = axes('Parent',figure1);
% hold(axes1,'on');
% 
% % Create multiple lines using matrix input to bar
% bar1 = bar(y);
% set(bar1(1),'DisplayName','Arch 2','FaceColor',[0 0.45 0.74]);
% set(bar1(2),'DisplayName','Arch 3','FaceColor',[0.85 0.33 0.01]);
% set(bar1(3),'DisplayName','Arch 4','FaceColor',[0.93 0.69 0.13]);
% 
% % Create xlabel
% xlabel(xlabel1, 'fontsize', 14);
% 
% % Create ylabel
% ylabel(ylabel1, 'fontsize', 14);
% 
% % Create title
% % title(title1);
% 
% box(axes1,'on');
% % Set the remaining axes properties
% set(axes1,'XGrid','on','XTick',[1 2 3],'XTickLabel',{'100','150','200'},...
%     'YGrid','on');
% a=[cellstr(num2str(get(gca,'ytick')'*100))];
% pct = char(ones(size(a,1),1)*'%');
% new_yticks = [char(a),pct];
% set(gca,'yticklabel',new_yticks) 
% 
% legend1 = legend(axes1,'show');
% set(legend1,'FontSize',16,'Location','east');
% 
% saveas(figure1, 'optGapCnk.jpg')
%%
arch2_FF_bwd_thpgap_pod100 = 0.9559;
arch2_FF_bwd_thpgap_pod150 = 0.9696;
arch2_FF_bwd_thpgap_pod200 = 0.9751;

arch4_FF_bwd_thpgap_pod100 = 0.9657;
arch4_FF_bwd_thpgap_pod150 = 0.9672;
arch4_FF_bwd_thpgap_pod200 = 0.9664;

arch5_FF_bwd_thpgap_pod100 = 0.9286;
arch5_FF_bwd_thpgap_pod150 = 0.9636;
arch5_FF_bwd_thpgap_pod200 = 0.9755;

y = 1-...
    [arch2_FF_bwd_thpgap_pod100, arch4_FF_bwd_thpgap_pod100, arch5_FF_bwd_thpgap_pod100;...
    arch2_FF_bwd_thpgap_pod150, arch4_FF_bwd_thpgap_pod150, arch5_FF_bwd_thpgap_pod150;...
    arch2_FF_bwd_thpgap_pod200, arch4_FF_bwd_thpgap_pod200, arch5_FF_bwd_thpgap_pod200];
title1 = 'Ascending First Fit in Architecture 2 with Connection Optimized';
xlabel1 = 'Number of PODs';
ylabel1 = 'Optimality gap';

figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'on');

% Create multiple lines using matrix input to bar
bar1 = bar(y);
set(bar1(1),'DisplayName','A1','FaceColor',[0.93 0.69 0.13]);
set(bar1(2),'DisplayName','A2','FaceColor',[0.85 0.33 0.01]);
set(bar1(3),'DisplayName','A3','FaceColor',[0 0.45 0.74]);

% Create xlabel
xlabel(xlabel1, 'fontsize', 18);

% Create ylabel
ylabel(ylabel1, 'fontsize', 18);

% Create title
% title(title1);

box(axes1,'on');
% Set the remaining axes properties
set(axes1,'XGrid','on','XTick',[1 2 3],'XTickLabel',{'100','150','200'},...
    'YGrid','on');
ytick = get(gca, 'ytick');
set(gca, 'ytick', ytick(1:2:end));
a=[cellstr(num2str(get(gca,'ytick')'*100))];
pct = char(ones(size(a,1),1)*'%');
new_yticks = [char(a),pct];
set(gca,'yticklabel',new_yticks) 
set(axes1, 'fontsize', 14)
set(axes1, 'gridalpha', 0.5)

legend1 = legend(axes1,'show');
set(legend1,'FontSize',16,'Location','northwest');
saveas(figure1, 'optGapthp.jpg')