import numpy as np
import pandas as pd
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

def bootstrap_CI_gamma(t, size=1000):
    '''
    Computes 95% confidence intervals using bootstrapped samples.
    '''
    bs_reps = bebi103.draw_bs_reps_mle(
        mle_fun=gamma_mle, 
        gen_fun=gen_gamma,
        data=t, 
        size=size, 
        progress_bar=True,
    )
    
    gamma_ci = np.percentile(bs_reps, [2.5, 97.5], axis=0)
    
    print(f'α 95% confidence interval: [{gamma_ci[0][0]:.3f}, {gamma_ci[1][0]:.3f}]')
    print(f'β 95% confidence interval: [{gamma_ci[0][1]:.3f}, {gamma_ci[1][1]:.3f}]')
    
def log_like_custom(params, t):
    '''
    Log likelihood for two Poisson processes distribution.
    '''
    beta_1, delta_beta = params

    n = len(t)

    if delta_beta < 0 or beta_1 <= 0:
        return -np.inf
    
    if delta_beta < 1e-9:
        return 2 * n * np.log(beta_1) + np.sum(np.log(t)) - beta_1 * np.sum(t)

    out = n * (np.log(beta_1) + np.log(beta_1 + delta_beta) - np.log(delta_beta))
    out -= beta_1 * np.sum(t)
    
    return out + np.sum(np.log(1 - np.exp(-delta_beta * t)))

def custom_mle(t):
    '''
    Perform MLE estimates for Gamma distribution parameters.
    '''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        res = scipy.optimize.minimize(
            lambda params, t: -log_like_custom(params, t),
            np.array([0.005, 0.001]),
            args=(t,),
            method="powell"
        )
    
    if res.success:
        return res.x
    else:
        raise RuntimeError('Convergence failed with message', res.message)
        
def aic_model_comp(t, alpha_mle, beta_mle, beta_1, beta_2):
    model_comparison = pd.DataFrame(index = [0,1],
                                    columns = ["model", "alpha", "beta", "beta 1", "beta 2", "log like", 
                                               "AIC", "AIC weight"])
    model_comparison["model"] = ["gamma", "2-step poisson"]
    model_comparison["alpha"][0] = alpha_mle
    model_comparison["beta"][0] = beta_mle
    model_comparison["beta 1"][1] = beta_1
    model_comparison["beta 2"][1] = beta_2

    model_comparison["log like"][0] = log_like_gamma([alpha_mle,beta_mle], t)
    model_comparison["log like"][1] = log_like_custom([beta_1,beta_2], t)

    model_comparison["AIC"][0] = -2 * model_comparison["log like"][0] + 4
    model_comparison["AIC"][1] = -2 * model_comparison["log like"][1] + 4


    max_aic = max(model_comparison["AIC"])
    gamma_aic = -2 * model_comparison["log like"][0] + 4
    two_step_poisson_aic = -2 * model_comparison["log like"][1] + 4
    num = np.exp(-(gamma_aic-max_aic)/2)
    denom = np.exp(-(gamma_aic-max_aic)/2)+(np.exp(-(two_step_poisson_aic-max_aic)/2))
    model_comparison["AIC weight"][0] = num / denom
    model_comparison["AIC weight"][1] = 1 - num / denom

    return model_comparison
        
