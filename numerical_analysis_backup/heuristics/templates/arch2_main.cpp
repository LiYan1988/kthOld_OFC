#include "arch2.h"

int main()
{
    srand(0);
    float load = 0.2;
    int tfk_mean = 200;
    int tfk_var = 100;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 3;
    int num_specs = 120;
    float Tmax = 2.5;
    float Tmin = 0.5;
    float alpha = 0.9999;
    int Smax = 50;
    int step_ini = 50;
    float step_delta = 0.95;
    int n_iter_ini = 100;
    float n_iter_delta = 1.05;
    float prob1 = 0.8;
    float prob2 = 1;

    int num_pods = 100;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    string trafficname = "simu1";
    for(int id=0; id<1; ++id){
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "simu1_matrix_"+to_string(id)+".csv";
        cout<<filename<<endl;
        t.read_traffic(filename);
        int e1, e2;
        ConnectionList l(t.connection_list.begin(), t.connection_list.end());
        reverse(l.begin(), l.end());
        Energy_is(t.connection_list, num_pods, num_cores, num_specs, e1);
        Energy_is(l, num_pods, num_cores, num_specs, e2);
        cout<<e1<<"|"<<e2<<"|"<<t.num_cnk<<endl;
        t.set_probs(prob1, prob2);
        t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
        // t.choose_stepsize(step_ini, 3, 50);
        bool flag_write = true;
        t.sa_is(t.connection_list, flag_write);
        // t.write_result();
    }   
}

