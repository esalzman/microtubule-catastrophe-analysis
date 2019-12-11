import numpy as np
import scipy.optimize
import scipy.stats as st

import warnings

def log_like_gamma(params, t):
    '''
    Log likelihood for a Gamma distribution.
    '''
    alpha, beta = params
    
    if alpha <= 0 or beta <= 0:
        return -np.inf
    
    return st.gamma.logpdf(t, alpha, loc=0, scale=1/beta).sum()

def gamma_mle(t):
    '''
    Perform MLE estimates for Gamma distribution parameters.
    '''
    # Initial guess
    t_bar = np.mean(t)
    beta_guess = t_bar / np.var(t)
    alpha_guess = t_bar * beta_guess

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        res = scipy.optimize.minimize(
            lambda params, t: -log_like_gamma(params, t),
            (alpha_guess, beta_guess),
            args=(t,),
            method="powell",
        )

    if res.success:
        return res.x
    else:
        raise RuntimeError('Convergence failed with message', res.message)
        
