### Raw and exact data

The files

`SK_model_p_1000_N_10_num_inst_10000_seed_137.h5`

etc. contain the raw data from the mean-field AOA. For `N=5, ..., 20`, these instances are identical to the exact instances in

`SK_model_p_1000_N_10_num_inst_10000_seed_137_exact.h5`,

i.e. they are obtained by restarting the notebook for each value of `N`, such that the seed is 137 at the beginning of each loop over the 10000 instances.


### Statistics

The files

`SK_model_p_1000_N_20_num_inst_10000_seed_137_hist_stats.h5`

contain the values of $`E_*`$ for each separate instance. The files

`SK_model_p_1000_N_10_num_inst_10000_seed_137_moments.h5`

in turn contain $`\langle E_*\rangle`$ and $`\langle E_*^2\rangle`$, i.e. the cost function averaged over all instances.
