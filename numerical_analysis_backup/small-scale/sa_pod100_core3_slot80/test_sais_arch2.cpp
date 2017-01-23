#include "sa_sdm.h"

int main()
{
    srand(0);
    float load = 0.2;
    int tfk_mean = 200;
    int tfk_var = 200;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 3;
    int num_specs = 80;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 300;
    int step_ini = 50;
    float step_delta = 0.99;
    int n_iter_ini = 10;
    float n_iter_delta = 1.05;
    float prob1 = 0.8;
    float prob2 = 1;

    int num_pods = 100;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    Row arch2_bench1, arch2_bench2, arch2_sa;
    Row arch4_bench1, arch4_bench2, arch4_sa;
    Row arch5_bench1, arch5_bench2, arch5_sa;

    string trafficname = "traffic_matrix_";
    for(int id=0; id<20; ++id){
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
        cout<<filename<<endl;
        t.read_traffic(filename,25);

        int num_cnk = t.num_cnk;
        cout<<num_cnk<<endl;

        /*SA*/
        int ea1s, ea2s, ea4s, ea5s;
        t.set_probs(prob1, prob2);
        t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
        // t.choose_stepsize(step_ini, 3, 50);
        bool flag_write = true;
        ConnectionList l{t.connection_list.begin(), t.connection_list.end()};
        // reverse(l.begin(),l.end());
        t.sais_arch4(l, flag_write, ea4s);
        arch4_sa.push_back(num_cnk-ea4s);
        cout<<arch4_sa[id]<<endl;
    }
}
