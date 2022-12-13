The instances for `N=5, ..., 20` are identical to those used in

`/home/lappet/Archives/projects/QuantumComputing/meanfieldaoa/data/SK_model/`,

i.e. they are obtained by restarting the notebook for each value of `N`, such that the seed is 137 at the beginning of each loop over the 10000 instances.


The files

`SK_model_p_1000_N_10_num_inst_10000_seed_137.h5`

etc. contain the raw data from the mean-field AOA. The files

`SK_model_p_1000_N_20_num_inst_10000_seed_137_hist_stats.h5`

contain the values of $`E_*`$ for each separate instances. The files

`SK_model_p_1000_N_10_num_inst_10000_seed_137_moments.h5`

in turn contain $`\langle E_*\rangle`$ and $`\langle E_*^2\rangle`$, i.e. the cost function averaged over all instances.
