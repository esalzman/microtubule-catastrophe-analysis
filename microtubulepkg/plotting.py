import numpy as np
import pandas as pd
import scipy.stats as st
import bokeh_catplot

from bokeh.models.annotations import Title

import holoviews as hv
hv.extension('bokeh')

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
    
def plot_all_concentrations(tub_df, mle_data):
    t = tub_df.loc[tub_df["concentration (int)"] == 7]["catastrophe time"].values
    alpha_mle, beta_mle = mle_data["alpha MLE"][0], mle_data["beta MLE"][0]

    p7 = bokeh_catplot.ecdf(pd.DataFrame({'t (s)': t}), val='t (s)', conf_int=True, x_axis_label='catastrophe time (s)')

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p7.line(t_theor, cdf, line_width=2, color='orange')
    
    title7 = Title()
    title7.text = '7 uM tubulin'
    p7.title = title7

    t = tub_df.loc[tub_df["concentration (int)"] == 9]["catastrophe time"].values
    alpha_mle, beta_mle = mle_data["alpha MLE"][1], mle_data["beta MLE"][1]

    p9 = bokeh_catplot.ecdf(pd.DataFrame({'t (s)': t}), val='t (s)', conf_int=True, x_axis_label='catastrophe time (s)')

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p9.line(t_theor, cdf, line_width=2, color='orange')
    
    title9 = Title()
    title9.text = '9 uM tubulin'
    p9.title = title9

    t = tub_df.loc[tub_df["concentration (int)"] == 10]["catastrophe time"].values
    alpha_mle, beta_mle = mle_data["alpha MLE"][2], mle_data["beta MLE"][2]

    p10 = bokeh_catplot.ecdf(pd.DataFrame({'t (s)': t}), val='t (s)', conf_int=True, x_axis_label='catastrophe time (s)')

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p10.line(t_theor, cdf, line_width=2, color='orange')
    
    title10 = Title()
    title10.text = '10 uM tubulin'
    p10.title = title10

    t = tub_df.loc[tub_df["concentration (int)"] == 12]["catastrophe time"].values
    alpha_mle, beta_mle = mle_data["alpha MLE"][3], mle_data["beta MLE"][3]

    p12 = bokeh_catplot.ecdf(pd.DataFrame({'t (s)': t}), val='t (s)', conf_int=True, x_axis_label='catastrophe time (s)')

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p12.line(t_theor, cdf, line_width=2, color='orange')

    title12 = Title()
    title12.text = '12 uM tubulin'
    p12.title = title12

    t = tub_df.loc[tub_df["concentration (int)"] == 14]["catastrophe time"].values
    alpha_mle, beta_mle = mle_data["alpha MLE"][4], mle_data["beta MLE"][4]

    p14 = bokeh_catplot.ecdf(pd.DataFrame({'t (s)': t}), val='t (s)', conf_int=True, x_axis_label='catastrophe time (s)')

    t_theor = np.linspace(0, 2000, 200)
    cdf = st.gamma.cdf(t_theor, alpha_mle, loc=0, scale=1/beta_mle)
    p14.line(t_theor, cdf, line_width=2, color='orange')
    
    title14 = Title()
    title14.text = '14 uM tubulin'
    p14.title = title14

    l = bokeh.layouts.layout([[p7,p9],[p10,p12],[p14]])

    bokeh.io.show(l)