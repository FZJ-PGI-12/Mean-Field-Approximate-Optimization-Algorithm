# MeanFieldAOA - Mean-Field Approximate Optimization Algorithm

#### A quantum-inspired classical optimization algorithm for Ising-like optimization problems

[arXiv:2303.00329](https://arxiv.org/abs/2303.00329)

## Abstract

The Quantum Approximate Optimization Algorithm (QAOA) is suggested as a promising appli-
cation on early quantum computers. Here, a quantum-inspired classical algorithm, the mean-field
Approximate Optimization Algorithm (mean-field AOA), is developed by replacing the quantum
evolution of the QAOA with classical spin dynamics through the mean-field approximation. Due to
the alternating structure of the QAOA, this classical dynamics can be found exactly for any number
of QAOA layers. We benchmark its performance against the QAOA on the Sherrington-Kirkpatrick
(SK) model and the partition problem, and find that the mean-field AOA outperforms the QAOA
in both cases for most instances. Our algorithm can thus serve as a tool to delineate optimization
problems that can be solved classically from those that cannot, i.e. we believe that it will help to
identify instances where a true quantum advantage can be expected from the QAOA. To quantify
quantum fluctuations around the mean-field trajectories, we solve an effective scattering problem in
time, which is characterized by a spectrum of time-dependent Lyapunov exponents. These provide
an indicator for the hardness of a given optimization problem relative to the mean-field AOA.


## Code

For an introduction to using the mean-field AOA code in this repository, please look into our [introductory notebook](notebooks/introduction.ipynb).

The remaining [notebooks](notebooks) can be used to reproduce the plots of our paper from the [data](data). Note that some of the notebooks are _written in Julia_. 


## Citation

If you are using code from this repository, please cite our work:
```
@article{PRXQuantum.4.030335,
  title = {Mean-Field Approximate Optimization Algorithm},
  author = {Misra-Spieldenner, Aditi and Bode, Tim and Schuhmacher, Peter K. and Stollenwerk, Tobias and Bagrets, Dmitry and Wilhelm, Frank K.},
  journal = {PRX Quantum},
  volume = {4},
  issue = {3},
  pages = {030335},
  numpages = {19},
  year = {2023},
  month = {Sep},
  publisher = {American Physical Society},
  doi = {10.1103/PRXQuantum.4.030335},
  url = {https://link.aps.org/doi/10.1103/PRXQuantum.4.030335}
}
```

