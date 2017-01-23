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
    int Smax = 50;
    int step_ini = 100;
    float step_delta = 0.95;
    int n_iter_ini = 100;
    float n_iter_delta = 1.01;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 250;
    int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
    int max_cnk = 2*(num_pods-1)*load - min_cnk;

    string trafficname = "traffic_matrix_";
    int N=1;
    int M=1;
    Matrix total_cnk(N, Row(M, 0));
    Row sa_total(N,0);
    Matrix sa_result(N, Row(3, 0));
    for(int id=0; id<N; ++id){
        num_cores = 15+id;
        step_ini = num_pods;

        for(int rep=0; rep<M; ++rep){
            Traffic t(trafficname, num_cores-1, num_pods, max_cnk, min_cnk, load, tfk_mean, 
                tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
            string filename = "traffic_matrix__matrix_"+to_string(id)+".csv";
            cout<<filename<<endl;
            t.read_traffic(filename,25);
            sa_total[id] = t.num_cnk;

            int ea1s, ea2s, ea4s, ea5s;
            t.set_probs(prob1, prob2);
            t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
            bool flag_write = false;
            ConnectionList in_list = t.connection_list;
            t.sais_arch2(in_list, flag_write, ea2s);
            sa_result[id][0] = t.num_cnk-ea2s;
            t.sais_arch4(in_list, flag_write, ea4s);
            sa_result[id][1] = t.num_cnk-ea4s;
            t.sais_arch5(in_list, flag_write, ea5s);
            sa_result[id][2] = t.num_cnk-ea5s;
        }
    }
    string filename = "result_test2_core15.csv";
    cout<<filename<<endl;
    ofstream myfile;
    myfile<<"Arch2_sa,"<<"Arch4_sa,"<<"Arch5_sa,"<<"total_cnk,"<<endl;
    for(int id=0; id<N; ++id){
        myfile<<sa_result[id][0]<<","<<sa_result[id][1]<<","<<sa_result[id][2]<<","<<sa_total[id]<<endl;
    }
    myfile.close();
}
