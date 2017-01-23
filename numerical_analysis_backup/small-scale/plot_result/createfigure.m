function createfigure(xvector1, ymatrix1)
%CREATEFIGURE(XVECTOR1, YMATRIX1)
%  XVECTOR1:  bar xvector
%  YMATRIX1:  bar matrix data

%  Auto-generated by MATLAB on 20-Jun-2016 14:48:34

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'on');

% Create multiple lines using matrix input to bar
bar(xvector1,ymatrix1,'Parent',axes1);

% Create xlabel
xlabel('Number of PODs','FontSize',14);

% Create ylabel
ylabel('Established connections','FontSize',14);

box(axes1,'on');
% Set the remaining axes properties
set(axes1,'FontSize',12,'XTick',[100 150 200],'YGrid','on');