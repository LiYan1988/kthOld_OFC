#include "sa_sdm.h"

int main()
{
    srand(0);
    float load = 0.5;
    int tfk_mean = 200;
    int tfk_var = 100;
    int cpst_slot = 25;
    int gb_slot = 1;
    int num_cores = 3;
    int num_specs = 160;
    float Tmax = 5;
    float Tmin = 1;
    float alpha = 0.9999;
    int Smax = 50;
    int step_ini = 100;
    float step_delta = 0.99;
    int n_iter_ini = 100;
    float n_iter_delta = 1.05;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 150;
    int total_cnk = num_pods*(num_pods-1)*load;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    string trafficname = "simu1";
    for(int id=0; id<20; ++id){
        Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
            tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
        string filename = "tm_arch5.csv";
        t.generate_traffic();
        cout<<"simu "<<id<<": "<<t.num_cnk<<endl;
        int e1, e2, e3, e4, e5, e6, e7, e8;
        ConnectionList order = t.bench_ajmal_arch2(t.connection_list, e1);
        int msize=0;
        t.bench_ajmal_arch5(order, msize, e2);
        ConnectionList l{t.connection_list.begin(), t.connection_list.end()};
        reverse(l.begin(), l.end());
        Energy(l, num_pods, num_cores, num_specs, e3);
        Energy_arch5(l, num_pods, num_cores, num_specs, e4);
        cout<<e1<<" "<<e2<<" "<<e3<<" "<<e4<<endl;
        // ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
        // reverse(reverselist.begin(), reverselist.end());
        // Energy_arch5(t.connection_list, num_pods, num_cores, num_specs, e1);
        // Energy_arch5(reverselist, num_pods, num_cores, num_specs, e2);
        // Energy_arch5_is(t.connection_list, num_pods, num_cores, num_specs, e3);
        // Energy_arch5_is(reverselist, num_pods, num_cores, num_specs, e4);

        // cout<<e4<<endl;
        // Energy(t.connection_list, num_pods, num_cores, num_specs, e5);
        // Energy(reverselist, num_pods, num_cores, num_specs, e6);
        // Energy_is(t.connection_list, num_pods, num_cores, num_specs, e7);
        // Energy_is(reverselist, num_pods, num_cores, num_specs, e8);
        // cout<<e4<<"|"<<e8<<endl;
        // cout<<e1<<"|"<<e2<<"|"<<e3<<"|"<<e4<<"|"<<e5<<"|"<<e6<<"|"<<e7<<"|"<<e8<<endl;
        // cout<<t.num_cnk<<endl;
        /*SA*/
        // t.set_probs(prob1, prob2);
        // t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
        // // // t.choose_stepsize(step_ini, 3, 50);
        // bool flag_write = true;
        // // t.sa_is(t.connection_list, flag_write);
        // // flag_write = false;
        // t.sais_arch1(t.connection_list, flag_write);
        // t.sais_arch2(t.connection_list, flag_write);
        // t.sais_arch4(t.connection_list, flag_write);
        // t.sa_arch5(t.connection_list, flag_write);
        // t.write_result();
    }
}
