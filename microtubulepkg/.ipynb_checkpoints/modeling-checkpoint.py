import numpy as np
import scipy.optimize
import scipy.stats as st
import bebi103

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
        
        
def gen_gamma(params, size, rg):
    '''
    Generates bootstrap sample from generative model.
    '''
    alpha, beta = params
    return rg.gamma(alpha, 1 / beta, size=size)

def bootstrap_CI(t, size=1000):
    bs_reps = bebi103.draw_bs_reps_mle(
        mle_fun=gamma_mle, 
        gen_fun=gen_gamma, 
        data=t, 
        size=size, 
        progress_bar=True,
    )
    
    ci = np.percentile(bs_reps, [2.5, 97.5], axis=0)
    
    print(f'α 95% confidence interval: [{ci[0][0]:.3f}, {ci[1][0]:.3f}]')
    print(f'β 95% confidence interval: [{ci[0][1]:.3f}, {ci[1][1]:.3f}]')
        
