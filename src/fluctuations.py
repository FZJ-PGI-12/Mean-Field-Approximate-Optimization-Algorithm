import numpy as np
from meanfieldaoa import m, solution

def evolve_fluctuations(S: np.ndarray, J:np.ndarray,  τ:np.double, β: np.ndarray, γ: np.ndarray):

    N = S.shape[1] + 1
    p = β.shape[0]

    A = np.zeros((p, N - 1, N - 1), dtype=np.complex_)
    B = np.zeros((p, N - 1, N - 1), dtype=np.complex_)
    
    τ_3 = np.diag(np.concatenate((np.ones(N - 1), -np.ones(N - 1))))
    L = np.zeros((p, 2*(N - 1), 2*(N - 1)), dtype=np.complex_)

    omega = np.zeros((p, 2*(N - 1)))
    M = np.eye(2 * (N - 1))
    lyapunov_exponent = np.zeros((p, 2*(N - 1)))
    
    assert β.shape == γ.shape
    
    # helper function to construct A and B    
    n_ij_pm = lambda idx, pm: solution(S[-1][:, 2])[idx] * S[k][idx, 0] + pm * 1j * S[k][idx, 1]    
        
    for k in range(γ.shape[0]):    
        
        for i in range(N - 1):
            # we exclude the factor of 2 here because we symmetrize below
            A[k][i][i] = β[k] * S[k][i, 0] / (1 + solution(S[-1][:, 2])[i] * S[k][i, 2]) + γ[k] * solution(S[-1][:, 2])[i] * m(S[k], J)[i]
            for j in range(i + 1, N - 1):
                A[k][i][j] = -γ[k] * J[i][j] * n_ij_pm(i, 1) * n_ij_pm(j, -1)
                B[k][i][j] = -γ[k] * J[i][j] * n_ij_pm(i, 1) * n_ij_pm(j,  1)
        
        # symmetrize
        A[k] += A[k].conj().T 
        B[k] += B[k].T 
        
        L[k] = τ_3@np.block([
                            [A[k], B[k]],
                            [B[k].conj().T, A[k].conj()]
                          ])
        
        omega_eig, omega_eigvec = np.linalg.eig(L[k])
        omega[k] = omega_eig.real        

        M = omega_eigvec @ np.diag(np.exp(-1j * τ * omega_eig)) @ np.linalg.inv(omega_eigvec) @ M
        lyapunov_exponential_eig, _ = np.linalg.eigh(M @ M.conj().T)
        lyapunov_exponent_eig = np.log(lyapunov_exponential_eig)/2

        lyapunov_exponent_eig = np.sort(lyapunov_exponent_eig)
        lyapunov_exponent[k] = lyapunov_exponent_eig

    omega = np.transpose(omega)
    lyapunov_exponent_t = np.transpose(lyapunov_exponent)
    lyapunov_exponent_t = np.flip(lyapunov_exponent_t, axis=0)
        
    return omega, lyapunov_exponent_t