#include "sa_sdm.h"

int main()
{
    srand(0);
    float load = 0.5;
    int tfk_mean = 200;
    int tfk_var = 200;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 10;
    int num_specs = 320;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 35;
    int step_ini = 200;
    float step_delta = 0.95;
    int n_iter_ini = 40;
    float n_iter_delta = 1;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 250;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    int id = 0;
    string trafficname = "test_sa_core";
    Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
        tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
    string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
    cout<<filename<<endl;
    t.generate_traffic();

    int ea1s, ea2s, ea4s, ea5s;
    t.set_probs(prob1, prob2);
    t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
    bool flag_write = false;
    ConnectionList in_list = t.connection_list;
    t.sais_arch2(in_list, flag_write, ea2s);
    t.sais_arch5(in_list, flag_write, ea5s);
}
