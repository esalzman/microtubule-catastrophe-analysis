import pandas as pd
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
        style='staircase'
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