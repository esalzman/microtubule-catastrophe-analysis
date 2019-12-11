import numpy as np
import pandas as pd
import scipy.stats as st
import bokeh_catplot

import holoviews as hv

import bokeh.io
bokeh.io.output_notebook()


def plot_ecdf(tub_df):
    '''
    Plots ECDFs for catastrophe time at different concentrations.
    '''
    p = bokeh_catplot.ecdf(
        data=tub_df,
        cats=['concentration'],
        val='catastrophe time',
        style='staircase',
        x_axis_label='catastrophe time (s)'
    )

    p.legend.location = 'bottom_right'

    bokeh.io.show(p)
    
def plot_box(tub_df):
    '''
    Plot boxplot for catastrophe time at different concentrations.
    '''
    box = bokeh_catplot.box(
        data=tub_df,
        cats=['concentration'],
        val='catastrophe time',
    )

    bokeh.io.show(box)
    
def plot_model_gamma(t, alpha_mle, beta_mle):
    '''
    Plots generative Gamma distribution against ECDF of data.
    '''
    p = bokeh_catplot.ecdf(
        pd.DataFrame({'t (s)': t}), 
        val='t (s)', 
        conf_int=True, 
        x_axis_label='catastrophe time (s)',
    )

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p.line(t_theor, cdf, line_width=2, color='orange')
    
    bokeh.io.show(p)
    
def plot_model_custom(t, beta_1, beta_2):
    '''
    Plots generative custom distribution against ECDF of data.
    '''
    t_theor = np.linspace(0, 2000, 200)
    cdf = (
        beta_1 * beta_2 / (beta_2 - beta_1)
        * (
            (1 - np.exp(-beta_1 * t_theor)) / beta_1
            - (1 - np.exp(-beta_2 * t_theor)) / beta_2
        )
    )

    p = bokeh_catplot.ecdf(data=pd.DataFrame({"t": t}), val="t", conf_int=True)
    p.line(t_theor, cdf, line_width=2, color="orange")

    bokeh.io.show(p)