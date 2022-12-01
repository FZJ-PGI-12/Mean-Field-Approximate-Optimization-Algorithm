import numpy as np
import sys
sys.path.append('../src')
from mf_AOA import evolve, expectation, solution

def test_SK_model():
    # schedule
    p = 10
    τ = 0.5
    γ = τ * (np.arange(1, p + 1) - 1/2) / p
    β = τ * (1 - np.arange(1, p + 1) / p)
    β[p-1] = τ / (4 * p)

    # initial spins
    N = 5
    S = np.array([[1., 0., 0.] for _ in range(N - 1)]) # fix final spin (i.e. leave it out)

    # SK model
    np.random.seed(11)
    J = np.random.normal(0, 1, size=(N, N)) / np.sqrt(N)
    J = np.triu(J, k=1)
    J = J + J.transpose()

    # evolution
    S = evolve(S, J, β, γ)
    
    # solution
    S_test = np.array([[-0.4280189887648497, -0.4161436735954462, -0.3151885316091266, 0.06825210700086091], 
                   [0.57845514021309, 0.1965348184395327, -0.14809317283731896, -0.5908423629410464], 
                   [0.6943985858408479, -0.8878054449413042, -0.9374031159010826, -0.8038948638001017]])
    
    assert np.allclose(S, S_test.T)
    assert np.allclose(expectation(S[:, 2], J), -2.5367551470078142)
    assert np.allclose(solution(S[:, 2]), [ 1., -1., -1., -1.])
    
test_SK_model()