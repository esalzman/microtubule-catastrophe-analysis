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
    p = bokeh_catplot.ecdf(
        pd.DataFrame({'t (s)': t}), 
        val='t (s)', 
        conf_int=True, 
        x_axis_label='catastrophe time (s)',
        #legend='Experimental data'
    )

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p.line(t_theor, cdf, line_width=2, color='orange', legend_label='Theoretical gamma distribution')
    
    p.legend.location = 'bottom_right'
    
    bokeh.io.show(p)