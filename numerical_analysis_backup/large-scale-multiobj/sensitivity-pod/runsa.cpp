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
    int Smax = 1; //10
    int step_ini = 200;
    float step_delta = 0.95;
    int n_iter_ini = 1; //2
    float n_iter_delta = 1;
    float prob1 = 1;
    float prob2 = 1;

    int num_pods = 250;

    string trafficname = "traffic_matrix_";
    int N=11; //23
    int M=3; //15
    Matrix total_cnk(N, Row(M, 0));
    Matrix arch2_bench1(N, Row(M, 0)), arch2_bench2(N, Row(M, 0)), arch2_sa(N, Row(M, 0));
    Matrix arch4_bench1(N, Row(M, 0)), arch4_bench2(N, Row(M, 0)), arch4_sa(N, Row(M, 0));
    Matrix arch5_bench1(N, Row(M, 0)), arch5_bench2(N, Row(M, 0)), arch5_sa(N, Row(M, 0));
    for(int id=0; id<N; ++id){
        num_pods = 100+id*50; // 100+id*25;
		int min_cnk = max(float(1), 2*(num_pods-1)*load-num_pods);
		int max_cnk = 2*(num_pods-1)*load - min_cnk;
        step_ini = num_pods;

        for(int rep=0; rep<M; ++rep){
            Traffic t(trafficname, id, num_pods, max_cnk, min_cnk, load, tfk_mean, 
                tfk_var, cpst_slot, gb_slot, num_cores, num_specs);
            t.generate_traffic();
            t.write_matrix();

            total_cnk[id][rep] = t.num_cnk;
            cout<<total_cnk[id][rep]<<endl;
            int num_cnk = total_cnk[id][rep];

            int ea2b1, ea2b2, ea4b1, ea4b2, ea5b1, ea5b2;
            ConnectionList reverselist{t.connection_list.begin(), t.connection_list.end()};
            reverse(reverselist.begin(), reverselist.end());
            ConnectionList in_list{t.connection_list.begin(), t.connection_list.end()};

            Energy_arch2(reverselist, num_pods, num_cores, num_specs,ea2b1);
            arch2_bench1[id][rep] = num_cnk-ea2b1;
            Energy_arch4(reverselist, num_pods, num_cores, num_specs, ea4b1);
            arch4_bench1[id][rep] = num_cnk-ea4b1;
            Energy_arch5(reverselist, num_pods, num_cores, num_specs, ea5b1);
            arch5_bench1[id][rep] = num_cnk-ea5b1;
            cout<<arch2_bench1[id][rep]<<"|"<<arch4_bench1[id][rep]<<"|"<<arch5_bench1[id][rep]<<endl;

            ConnectionList order = t.bench_ajmal_arch2(reverselist, ea2b2);
            arch2_bench2[id][rep] = num_cnk-ea2b2;
            t.bench_ajmal_arch4(reverselist, ea4b2);
            arch4_bench2[id][rep] = num_cnk-ea4b2;
            t.bench_ajmal_arch5(order, 0, ea5b2);
            arch5_bench2[id][rep] = num_cnk-ea5b2;
            cout<<arch2_bench2[id][rep]<<"|"<<arch4_bench2[id][rep]<<"|"<<arch5_bench2[id][rep]<<endl;

            /*SA*/
            int ea1s, ea2s, ea4s, ea5s;
            t.set_probs(prob1, prob2);
            t.schedule(Tmax, Tmin, Smax, alpha, step_ini, step_delta, n_iter_ini, n_iter_delta);
            bool flag_write = false;
            in_list = t.connection_list;
            t.sais_arch2(in_list, flag_write, ea2s);
            arch2_sa[id][rep] = num_cnk-ea2s;
            in_list = t.connection_list;
            t.sais_arch4(in_list, flag_write, ea4s);
            arch4_sa[id][rep] = num_cnk-ea4s;
            in_list = t.connection_list;
            t.sais_arch5(in_list, flag_write, ea5s);
            arch5_sa[id][rep] = num_cnk-ea5s;
            cout<<arch2_sa[id][rep]<<"|"<<arch4_sa[id][rep]<<"|"<<arch5_sa[id][rep]<<endl;
        }
        ostringstream ss;
        ss<<id;
        string filename = "result_sa_core"+ss.str()+".csv";
        cout<<filename<<endl;
        ofstream myfile;
        myfile.open(filename);
        myfile<<"Arch2_bench1,"<<"Arch2_bench2,"<<"Arch2_sa,"<<"Arch4_bench1,"<<"Arch4_bench2,"<<"Arch4_sa,"<<"Arch5_bench1,"<<"Arch5_bench2,"<<"Arch5_sa,"<<"total_cnk,"<<endl;
        for(int rep=0; rep<M; ++rep){
            myfile<<arch2_bench1[id][rep]<<","<<arch2_bench2[id][rep]<<","<<arch2_sa[id][rep]<<","<<arch4_bench1[id][rep]<<","<<arch4_bench2[id][rep]<<","<<arch4_sa[id][rep]<<","<<arch5_bench1[id][rep]<<","<<arch5_bench2[id][rep]<<","<<arch5_sa[id][rep]<<","<<total_cnk[id][rep]<<","<<endl;
        }
        myfile.close();
    }
}
