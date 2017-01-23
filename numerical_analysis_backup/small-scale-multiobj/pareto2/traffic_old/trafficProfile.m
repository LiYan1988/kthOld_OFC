function [x] = trafficProfile(f, Nele, Tele, lbf)
    r = (1-Nele)/Nele;
    t = Tele/(1-Tele);
    Aeq = [[1, 1, 1, 1, -r, -r];...
        [t*[1, 10, 100, 200], -400, -1000];...
        ones(1, 6)];
    beq = [zeros(2, 1); 1];
    lb = lbf*ones(6, 1);
    ub = ones(6, 1);
    [x, fval, exitflag] = linprog(f,[],[],Aeq,beq,lb,ub);
    disp(x)
    