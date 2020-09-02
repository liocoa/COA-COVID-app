# -*- coding: utf-8 -*-

# Importable module for making the plots.
# I just prefer to have these in a separate place to avoid clutter.

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



#Campus population
POP = 480

# Column names
# Included in data entry
start = "Start date"
end = "End date"
tested = "Total tests"
positive = "Positive tests"
new = "New cases"
recovered = "Recovered cases"
isol = "Number in isolation"
quar = "Number in quarantine"
# Calculated
negative = "Negative results"
active = "Active cases"


def calculate(df):
	# Calculate negative cases
	df[negative]=df[tested]-df[positive]

	# Calcuate active cases
	active_cases = np.zeros(len(df)).astype(int)
	active_cases[0] = df[new][0]
	for i in range(len(df)-1):
	    active_cases[i+1] = active_cases[i] + df[new][i+1] - df[recovered][i+1]
	df[active] = active_cases

	# Check that active cases == current isolations?

	return df

def timeseries(df):
	fig = px.line(df,x=end,y=active,range_y=(0,POP/3),title="Active cases over time")
	fig.update_layout(title={"text":"Active cases over time","x":0.5,"xanchor":"center"}, showlegend=False)
	return fig

def make_donut(values,hole_number,title,fine_print):

	donut_margins = dict(l=30, r=20, t=40, b=10)

	fig = go.Figure(data=[go.Pie(values=values, hole=0.5)])

	# Title, suppress legend
	fig.update_layout(title={"text":title,"x":0.5,"xanchor":"center"}, showlegend=False)
	# Trace labels and hover info
	fig.update_traces(textinfo="none",hoverinfo='none')
	# Center data
	fig.add_annotation(text=f"{hole_number:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)
	# Fine print
	fig.add_annotation(text=fine_print, x=0.5, y=1, showarrow=False)
	# Margins
	fig.update_layout(margin=donut_margins)

	return fig

def donut_isol(df):
	current_isol_val = df[isol].iloc[-1]
	percent_isol = current_isol_val/POP*100
	isol_pie_values = [current_isol_val,POP-current_isol_val]

	title = "Current Isolations"
	fine_print = "*percent of total campus program participants"

	fig = make_donut(isol_pie_values,percent_isol,title,fine_print)

	return fig

def donut_quar(df):
	current_quar_val = df[quar].iloc[-1]
	percent_quar = current_quar_val/POP*100
	quar_pie_values = [current_quar_val,POP-current_quar_val]

	title = "Current Quarantines"
	fine_print = "*percent of on-campus housing residents"

	fig = make_donut(quar_pie_values,percent_quar,title,fine_print)    

	return fig

def donut_total_tests(df):
	total_tests = df[tested].sum()
	total_pos = df[positive].sum()
	percent_pos = total_pos/total_tests*100
	pos_pie_values = [total_pos,total_tests-total_pos]

	title = "Overall positive rate"
	fine_print = "*total percent of on-campus tests returned positive"

	fig = make_donut(pos_pie_values,percent_pos,title,fine_print)

	return fig

def make_table_df(df):
	labels = ["Total tested:", "Total negative:", "Positive rate:"]
	current_vals = [df[tested].iloc[-1],
	                df[negative].iloc[-1]]
	previous_vals = [df[tested].iloc[-2],
	                 df[negative].iloc[-2]]
	since_vals = [df[tested].sum(),
	              df[negative].sum()]

	for vals in [current_vals,previous_vals,since_vals]:
	    pos_rate = (vals[0]-vals[1])/vals[0]*100
	    vals.append(f"{pos_rate:.1f}%")

	data = pd.DataFrame({"":labels,"This week":current_vals,
	                   "Last week":previous_vals,f"Since {df[end].iloc[0]}":since_vals})
	return data


#def testing_rectangle(df):
	# # A graph for total + and - from campus testing

	# # Make a square whose area is equal to the number of tests conducted
	# total_tests = df[tested].sum()
	# test_side_length = np.sqrt(total_tests)

	# # Make a square whose area is equal to the number of positive results
	# total_pos = df[positive].sum()
	# pos_side_length = np.sqrt(total_pos)

	# # Make the graph
	# fig = go.Figure()

	# # Set axis properties (get rid of gridlines and axis scales)
	# fig.update_xaxes(range=[-0.1*test_side_length, 1.1*test_side_length], showgrid=False, zeroline=False, visible=False)
	# fig.update_yaxes(range=[-0.1*test_side_length, 1.1*test_side_length], showgrid=False, zeroline=False, visible=False)

	# # Other layout
	# fig.update_layout(title={"text":"Proportion of total tests that were positive","x":0.5,"xanchor":"center"})

	# # A shape for tests
	# fig.add_shape(type="rect",
	#              x0=0,
	#              y0=0,
	#              x1=test_side_length,
	#              y1=test_side_length,
	#              fillcolor="lightskyblue")

	# # A shape for positives
	# fig.add_shape(type="rect",
	#              x0=0,
	#              y0=0,
	#              x1=pos_side_length,
	#              y1=pos_side_length,
	#              fillcolor="firebrick")

	# return fig
