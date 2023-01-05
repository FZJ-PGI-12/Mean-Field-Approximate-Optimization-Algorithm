"""meanfieldaoa

Collection of functions implementing the mean-field AOA algorithm.

"""

import numpy as np

def rotation(alpha: np.ndarray) -> np.ndarray:
    """Computes an array of rotation matrices parametrized by the vector alpha.

    Args:
        alpha (np.ndarray, float):  vector of rotation angles or a scalar rotation angle

    Returns:
        np.ndarray: array of rotation matrices corresponding to the input angles
    """
    c, s = np.cos(alpha), np.sin(alpha)
    return np.array(((c, -s), (s, c))).T



def m(S: np.ndarray, J: np.ndarray) -> np.ndarray:
    """Computes the vector arising from the product of the interaction matrix J
    with the vector formed by all z-components of the spins S.

    Args:
        S (np.ndarray): matrix holding the x-,y- and z-components of all spins
        J (np.ndarray): interaction matrix

    Returns:
        np.ndarray: vector holding the results
    """
    
    N = S.shape[0] + 1
    
    return J[N-1, :-1] + J[:N-1, :N-1] @ S[:, 2]



def evolve(S: np.ndarray, J:np.ndarray,  β: np.ndarray, γ: np.ndarray):
    """Performs a mean-field AOA step by multiplying the spins by the problem and then the driver matrices.

    For a general understanding, please note that v = np.einsum("ijk,ik->ij", A, B]),
    where A.shape = (N, m, m) and B.shape = (N, m),
    is equivalent to v_{i, j} = A_{i, jk} B_{i, k}, where v.shape = (N, m).
    Here, N signifies the number of spins, while m=3 is the number of components per spin.

    Also, note that
    S[:, :2] gives the x- and y-directions of all spins,
    XY[:, 1:] gives the y-directions of all spins (after multiplication with the problem matrices),
    XY[:, :1] gives the x-directions of all spins (after multiplication with the problem matrices),
    S[:, 2:] gives the z-directions of all spins.


    np.concatenate((XY[:, 1:], S[:, 2:]), axis=1) gives the y- and z-directions of all spins,
    after the former have been multiplied by the problem matrices. In the return statement,
    these are then multiplied by the driver matrices and merged together with the deposited x-components of all spins.


    Args:
        S (np.ndarray): matrix holding the x-,y- and z-components of all spins
        problem (np.ndarray): array holding the problem matrices for all spins.
        driver (np.ndarray): array holding the driver matrices for all spins.

    Returns:
        np.ndarray: matrix holding the x-,y- and z-components of all spins
    """    
        
    N = S.shape[0] + 1        
        
    # evolution matrices
    V_D = lambda k: rotation(2 * β[k] * np.ones(N - 1))
    V_P = lambda k, m: rotation(2 * γ[k] * m)
    
    assert β.shape == γ.shape
    
    for k in range(γ.shape[0]):
        XY = np.einsum("ijk,ik->ij", V_P(k, m(S, J)), S[:, :2])
        S = np.concatenate((XY[:, :1],
                            np.einsum("ijk,ik->ij", V_D(k),
                                      np.concatenate((XY[:, 1:], S[:, 2:]), axis=1))
                           ), axis=1)
    return S



def expectation(S_z: np.ndarray, J: np.ndarray):
    """Returns the energy expectation value in the standard basis.
    
    Args:
        S (np.ndarray): vector holding the z-components of all spins
        J (np.ndarray): interaction matrix

    Returns:
        float: energy expectation value    
    """

    N = S_z.shape[0] + 1
    
    return -(J[N-1, :-1] + 0.5 * S_z @ J[:N-1, :N-1]) @ S_z



def solution(S_z: np.ndarray):
    """Returns the result of the algorithm, i.e. the rounded bitstring.

    Args:
        S (np.ndarray): vector holding the z-components of all spins
        
    Returns:
        np.ndarray: solution bitstring      
    """
    return np.sign(S_z)