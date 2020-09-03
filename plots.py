# -*- coding: utf-8 -*-

# Importable module for making the plots.
# I just prefer to have these in a separate place to avoid clutter.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_table



#Campus population
POP = 480
colors = {"COAblue":"#003399",
			"COAgreen":"#669999",
			"COVIDred":"#b20c28",
			"COAyellow":"#9e711c",
			"COAbrown": "#824b15"}

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

def maine_current(df):
	# Calculate current cases for Maine and Hancock
	df["CURRENT"] = df["CASES"] - df["DEATHS"] - df["RECOVERIES"]

	return df


def timeseries(df):
	fig = px.line(df,x=end,y=active,range_y=(0,1.25*df[active].max()),title="Active cases over time",labels={end:""})
	fig.update_layout(title={"text":"Active cases over time","x":0.5,"xanchor":"center"}, showlegend=False)
	# Margins
	fig.update_layout(height=300,margin=dict(l=30, r=30, t=40, b=0))
	# Line color
	fig.update_traces(line = dict(color=colors["COAblue"]))
	# Fonts
	fig.update_layout(font_family="Trebuchet MS")
	# Plot background
	fig.update_layout(plot_bgcolor="#ecf0f1")
	return fig


def make_donut(values,hole_number,title,fine_print):

	donut_margins = dict(l=30, r=30, t=40, b=10)



	fig = go.Figure(data=[go.Pie(values=values, hole=0.5)])

	# Title, suppress legend
	fig.update_layout(title={"text":title,"x":0.5,"xanchor":"center"}, showlegend=False)
	# Trace labels and hover info
	fig.update_traces(textinfo="none",hoverinfo='none')
	# Colors
	fig.update_traces(marker=dict(colors=[colors["COAblue"],colors["COAgreen"]]))
	# Center data
	fig.add_annotation(text=f"{hole_number:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)
	# Fine print
	fig.add_annotation(text=fine_print, x=0.5, y=1, showarrow=False)
	# Margins
	fig.update_layout(margin=donut_margins)
	# Fonts
	fig.update_layout(font_family="Trebuchet MS")

	return fig

def donut_isol(df):
	current_isol_val = df[isol].iloc[-1]
	percent_isol = current_isol_val/POP*100
	isol_pie_values = [current_isol_val,POP-current_isol_val]

	title = "Current Isolations"
	fine_print = "*percent of COA community currently in isolation"

	fig = make_donut(isol_pie_values,percent_isol,title,fine_print)

	return fig

def donut_quar(df):
	current_quar_val = df[quar].iloc[-1]
	percent_quar = current_quar_val/POP*100
	quar_pie_values = [current_quar_val,POP-current_quar_val]

	title = "Current Quarantines"
	fine_print = "*percent of COA community currently in quarantine"

	fig = make_donut(quar_pie_values,percent_quar,title,fine_print)    

	return fig

def donut_total_tests(df):
	total_tests = df[tested].sum()
	total_pos = df[positive].sum()
	percent_pos = total_pos/total_tests*100
	pos_pie_values = [total_pos,total_tests-total_pos]

	title = "Overall positive rate"
	fine_print = "*percent of all COA community tests returned positive"

	fig = make_donut(pos_pie_values,percent_pos,title,fine_print)

	return fig

def make_table_df(df):
	labels = ["Tests conducted:", "Positive results:", "Positivity rate:"]
	current_vals = [df[tested].iloc[-1],
	                df[positive].iloc[-1]]
	previous_vals = [df[tested].iloc[-2],
	                 df[positive].iloc[-2]]
	since_vals = [df[tested].sum(),
	              df[positive].sum()]

	for vals in [current_vals,previous_vals,since_vals]:
	    pos_rate = (vals[1])/vals[0]*100
	    vals.append(f"{pos_rate:.1f}%")

	data = pd.DataFrame({"":labels,"This week":current_vals,
	                   "Last week":previous_vals,f"Since {df[end].iloc[0]}":since_vals})


	return data

def reporting_table(df):
	daterange = lambda index : f"{df[start].iloc[index]} to {df[end].iloc[index]}"
	

	time_labels = [f"Current reporting period ({daterange(-1)})",f"Previous reporting period ({daterange(-2)})",f"Total since {df[start].iloc[0]}"]
	totals = [df[tested].iloc[-1],df[tested].iloc[-2],df[tested].sum()]
	positives = [df[positive].iloc[-1],df[positive].iloc[-2],df[positive].sum()]
	
	posrate = lambda idx : f"{positives[idx]/totals[idx]*100:.1f}%"
	pos_rates = [posrate(0),posrate(1),posrate(2)]

	data = pd.DataFrame({"":time_labels,"Tests conducted":totals,"Positive results":positives,"Positive rate":pos_rates})

	return data