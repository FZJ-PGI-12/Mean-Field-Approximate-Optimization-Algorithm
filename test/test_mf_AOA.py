import numpy as np
from scipy.integrate import solve_ivp
import sys
sys.path.append('../src')
from meanfieldaoa import evolve, expectation, solution

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



def test_time_evolution():
    # schedule
    T = 10.
    p = 2**10
    Δt = T/p

    # do not change N!
    N = 3
    J = np.triu(np.ones((N, N)), k=1) 
    J += J.transpose()      

    # fix final spin (i.e. leave it out)
    S = np.array([[1., 0., 0.] for _ in range(N - 1)]) 
    data = np.array([S for _ in range(p+1)])

    # get time-evolution data from algorithm
    for k in range(p):
        S = evolve(S, J, np.array([Δt]), np.array([Δt]))
        data[k + 1] = S    

    # function for the scipy time-stepper with hard-coded rhs for N-1=2 spins
    # first spin is y[0:3], second spin is y[3:6]
    def S(t, y, B, C):
        h = J[N-1, :-1]
        Δ = np.ones(N - 1)
        m_0 = h[0] + J[0, 1] * y[3 + 2]
        m_1 = h[1] + J[1, 0] * y[0 + 2]
        return [2 * C * m_0  * y[0 + 1], 
                2 * B * Δ[0] * y[0 + 2] - 2 * C * m_0 * y[0 + 0],
               -2 * B * Δ[0] * y[0 + 1],
                2 * C * m_1  * y[3 + 1], 
                2 * B * Δ[1] * y[3 + 2] - 2 * C * m_1 * y[3 + 0],
               -2 * B * Δ[1] * y[3 + 1]]

    init = [1., 0., 0., 1., 0., 0.]
    test_data = np.array([init for _ in range(p+1)])
    for i in range(p):
        # do a problem step
        sol = solve_ivp(S, [0, Δt], init, t_eval=[Δt], args=(0., 1.))
        init = sol.y.flatten()
        
        # then do a driver step
        sol = solve_ivp(S, [0, Δt], init, t_eval=[Δt], args=(1., 0.))
        init = sol.y.flatten()
        
        test_data[i+1] = sol.y.flatten()        

    digits = 7
    assert (np.round(data[:, 0, 0] - test_data.T[0], decimals=digits) == 0.0).all()
    assert (np.round(data[:, 0, 1] - test_data.T[1], decimals=digits) == 0.0).all()
    assert (np.round(data[:, 0, 2] - test_data.T[2], decimals=digits) == 0.0).all()        

# run tests    
test_SK_model()
test_time_evolution()