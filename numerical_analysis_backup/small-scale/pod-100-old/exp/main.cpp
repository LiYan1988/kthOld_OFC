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
    int num_specs = 160;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 20;
    int step_ini = 100;
    float step_delta = 0.98;
    int n_iter_ini = 10;
    float n_iter_delta = 1.05;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 100;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    string trafficname = "simu2";
    // for(int i=0; i<20; ++i){
    // 	Traffic t(trafficname, i, num_pods, max_cnk, min_cnk, load, tfk_mean, 
    //      tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
    //     t.generate_traffic();
    //     // t.write_matrix();
    //     int e1,e2;
    //     Energy_is(t.connection_list, num_pods, num_cores, num_specs, e1);
    //     Energy(t.connection_list, num_pods, num_cores, num_specs, e2);
    //     cout<<e1<<"|"<<e2<<endl;
    // }
 //    string trafficname = "exp";
    Traffic t(trafficname, 1, num_pods, max_cnk, min_cnk, load, tfk_mean, 
        tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
    string filename = "simu2_matrix_17.csv";
    t.read_traffic(filename);
    // t.show_traffic_matrix();
    // for(auto c: data) cout<<c<<endl;
	// t.generate_traffic();
 //    t.write_matrix();

    /*SA*/
    t.set_probs(prob1, prob2);
    t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
    // t.choose_stepsize(step_ini, 3, 50);
    bool flag_write = true;
    t.sa_is(t.connection_list, flag_write);
    // flag_write = false;
    // t.sa(t.connection_list, flag_write);


}

