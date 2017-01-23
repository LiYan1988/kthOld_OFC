function [x] = trafficProfile(f, Nele, Tele, lbf)
% Assume 1, 10, 100, 200 Gbps are mice flows, 400 and 1000 are elephants
% Nele is the percentage of elephant numbers
% Tele is the percentage of elephant throughput
% f is the objective, maximize certain type of traffic
% lbf is a number, each traffic type has at least this percentage
    r = (1-Nele)/Nele;
    t = Tele/(1-Tele);
    Aeq = [[1, 1, 1, 1, -r, -r];...
        [t*[1, 10, 100, 200], -400, -1000];...
        ones(1, 6)];
    beq = [zeros(2, 1); 1];
    lb = lbf*ones(6, 1);
    ub = ones(6, 1);
    options = optimoptions('linprog', 'Algorithm', 'interior-point-legacy');
    [x, fval, exitflag] = linprog(f,[],[],Aeq,beq,lb,ub,options);
    disp(x)
    