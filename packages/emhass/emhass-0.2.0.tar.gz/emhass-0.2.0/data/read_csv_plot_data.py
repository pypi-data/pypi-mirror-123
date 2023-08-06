# -*- coding: utf-8 -*-
'''
    This is a script for analysis plot.
    To use this script you will need plotly and kaleido. Install them using: 
        pip install plotly
        pip install kaleido
'''
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.io as pio
pio.renderers.default = 'browser'
pd.options.plotting.backend = "plotly"

from emhass.utils import get_root, get_logger

# the root folder
root = get_root()
# create logger
logger, ch = get_logger(__name__, root, file=False)

# Reading CSV files
path_file = "opt_res_perfect_optim_cost.csv"
data_cost = pd.read_csv(path_file, index_col='timestamp')
data_cost.index = pd.to_datetime(data_cost.index)
path_file = "opt_res_perfect_optim_profit.csv"
data_profit = pd.read_csv(path_file, index_col='timestamp')
data_profit.index = pd.to_datetime(data_profit.index)
path_file = "opt_res_perfect_optim_self-consumption.csv"
data_selfcons = pd.read_csv(path_file, index_col='timestamp')
data_selfcons.index = pd.to_datetime(data_selfcons.index)

# Creating DF to plot
cols_to_plot = ['P_PV', 'P_Load', 'P_def_sum_cost', 'P_def_sum_profit', 'P_def_sum_selfcons',
                'gain_cost', 'gain_profit', 'gain_selfcons']
data = pd.DataFrame(index=data_cost.index, columns=cols_to_plot)
data['P_PV'] = data_cost['P_PV']
data['P_Load'] = data_cost['P_Load']
data['P_def_sum_cost'] = data_cost['P_deferrable0']+data_cost['P_deferrable1']
data['P_def_sum_profit'] = data_profit['P_deferrable0']+data_profit['P_deferrable1']
data['P_def_sum_selfcons'] = data_selfcons['P_deferrable0']+data_selfcons['P_deferrable1']
data['gain_cost'] = data_cost['cost_profit']
data['gain_profit'] = data_profit['cost_profit']
data['gain_selfcons'] = data_selfcons['cost_profit']

# Meta parameters
symbols =['circle', 'square', 'diamond', 'star', 'triangle-left', 'triangle-right']
template = 'none'
symbol_size = 5
cf = ['cost', 'profit', 'selfcons']

# Plotting using plotly
this_figure = sp.make_subplots(rows=2, cols=1,
                               shared_xaxes=True, vertical_spacing=0.04,
                               subplot_titles=['System powers',
                                               'Cost function values'],
                               x_title="Date")

fig = px.line(data, x=data.index, y=cols_to_plot[0:5], markers=True,
              template = template)

fig.update_traces(marker=dict(size=symbol_size))

fig_traces = []
for trace in range(len(fig["data"])):
    trace_to_append = fig["data"][trace]
    trace_to_append.marker.symbol = symbols[trace]
    fig_traces.append(trace_to_append)
for traces in fig_traces:
    this_figure.append_trace(traces, row=1, col=1)

fig2 = px.line(data, x=data.index, y=cols_to_plot[5:], markers=False,
               template = template)

fig2.update_traces(marker=dict(size=symbol_size),
                   line=dict(dash='solid'))

fig_traces = []
for trace in range(len(fig2["data"])):
    trace_to_append = fig2["data"][trace]
    trace_to_append.marker.symbol = symbols[trace]
    fig_traces.append(trace_to_append)
for traces in fig_traces:
    this_figure.append_trace(traces, row=2, col=1)
# this_figure.update_yaxes(range=[49,51], row=2, col=1)

this_figure.layout.template = template
this_figure.show()

fig_filename = root + "/docs/images/optim_results"
this_figure.write_image(fig_filename + ".png", width=1080, height=0.75*1080)

fig_bar = px.bar(np.arange(len(cf)), x=[c+" (+"+"{:.2f}".format(np.sum(data['gain_'+c])*100/np.sum(
                     data['gain_profit'])-100)+")" for c in cf], 
                 y=[np.sum(data['gain_'+c]) for c in cf],
                 text=[np.sum(data['gain_'+c]) for c in cf], 
                 template = template)
fig_bar.update_yaxes(title_text="Cost function total value")
fig_bar.update_traces(texttemplate='%{text:.4s}', textposition='outside')
fig_bar.update_xaxes(title_text = "Cost function")
fig_bar.show()
fig_filename = root + "/docs/images/optim_results_bar_plot"
fig_bar.write_image(fig_filename + ".png", width=640, height=0.8*640)