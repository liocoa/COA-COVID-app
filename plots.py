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
POP = 492
colors = {"COAblue":"#003399",
			"COAgreen":"#669999",
			"COVIDred":"#b20c28",
			"COAyellow":"#9e711c",
			"COAbrown": "#824b15",
			"paperColor": "#ecf0f1"}

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
exp = "Positive explanation"

maine_pop = 1344212
hancock_pop = 54811

# pass to graph objects to make them static
config = {'staticPlot': True}


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

def maine_relevant_data(df):
	# Hancock county is the 14th line
	hancock_cases = df['cases'][13]
	total_cases = df["cases"].sum()

	data = {"PATIENT_COUNTY":["Hancock","Total"],
			"CASES":[hancock_cases,total_cases],
			"POP":[hancock_pop,maine_pop],
			"PERCAP":[hancock_cases/hancock_pop*10000,total_cases/maine_pop*10000]}

	df2 = pd.DataFrame(data)

	return df2


def timeseries(df):

	# Don't bother with the chart if we haven't had a single active case
	if df[active].sum() == 0:
		return None


	fig = px.line(df,x=end,y=active,range_y=(0,1.25*df[active].max()),title="Active cases over time",labels={end:""})
	fig.update_layout(title={"text":"Active cases over time","x":0.5,"xanchor":"center"}, showlegend=False)
	# Margins
	fig.update_layout(height=300,margin=dict(l=30, r=30, t=40, b=0))
	# Line color
	fig.update_traces(line = dict(color=colors["COAblue"]))
	# Fonts
	fig.update_layout(font_family="Trebuchet MS",font_size=18)
	# Plot background
	fig.update_layout(plot_bgcolor=colors["paperColor"])
	
	content = html.Div([
		dcc.Graph(
			id="timeseries-graph",
			figure=fig,
			config=config),
		html.Br()
		])



	return content


def make_donut(values,hole_number,title,fine_print):

	donut_margins = dict(l=20, r=20, t=0, b=0)

	fig = go.Figure(data=[go.Pie(values=values, hole=0.5)])

	# Title, suppress legend
	#fig.update_layout(title={"text":title,"x":0.5,"xanchor":"center"})
	fig.update_layout(showlegend=False)
	# Trace labels and hover info
	fig.update_traces(textinfo="none",hoverinfo='none')
	# Colors
	fig.update_traces(marker=dict(colors=[colors["COAblue"],colors["COAgreen"]]))
	# Plot background
	fig.update_layout(paper_bgcolor=colors["paperColor"])
	# Center data
	fig.add_annotation(text=f"{hole_number:.1f}%", x=0.5, y=0.5, font_size=30, showarrow=False)
	# Fine print
	# fig.add_annotation(text=fine_print, x=0.5, y=1, showarrow=False)
	# Margins
	fig.update_layout(margin=donut_margins)
	# Fonts
	fig.update_layout(font_family="Trebuchet MS",font_size=18)

	content = html.Div([
		html.Br(),
		html.H4(title,style={"textAlign":"center"}),
		html.H4(fine_print,style={"textAlign":"center"}),
		dcc.Graph(figure=fig,config=config),
		html.Br()
		],
		style={"backgroundColor":colors["paperColor"],
				"borderRadius":"5px"}
		)

	return content

def donut_isol(df):
	current_isol_val = df[isol].iloc[-1]
	percent_isol = current_isol_val/POP*100
	isol_pie_values = [current_isol_val,POP-current_isol_val]

	title = "Current Isolation"
	fine_print = str(current_isol_val)

	return make_donut(isol_pie_values,percent_isol,title,fine_print)


def donut_quar(df):
	current_quar_val = df[quar].iloc[-1]
	percent_quar = current_quar_val/POP*100
	quar_pie_values = [current_quar_val,POP-current_quar_val]

	title = "Current Quarantine"
	fine_print = str(current_quar_val)


	return make_donut(quar_pie_values,percent_quar,title,fine_print)    




def reporting_table(df):

	daterange = lambda index : f"{df[start].iloc[index]}–{df[end].iloc[index]}"

	# If there's only one line, just do total since

	if len(df) == 1:
		time_labels = [f"Total since {df[start].iloc[0]}"]
		totals = [df[tested].sum()]
		positives = [df[positive].sum()]
		
		posrate = lambda idx : f"{positives[idx]/totals[idx]*100:.1f}%"
		pos_rates = [posrate(0)]


	# If there's two or more lines, we can do the whole shebang
	else:
		time_labels = [f"Current reporting period ({daterange(-1)})",f"Previous reporting period ({daterange(-2)})",f"Total since 8/22/2020"]
		totals = [df[tested].iloc[-1],df[tested].iloc[-2],df[tested].sum()]
		positives = [df[positive].iloc[-1],df[positive].iloc[-2],df[positive].sum()]
		
		posrate = lambda idx : f"{positives[idx]/totals[idx]*100:.1f}%"
		pos_rates = [posrate(0),posrate(1),posrate(2)]


	# Either way, check for an interjection on either the current or previous reporting period
	if not pd.isnull(df[exp].iloc[-1]):
		positives[0] = f"{positives[0]}*"
	elif not pd.isnull(df[exp].iloc[-2]):
		positives[1] = f"{positives[1]}*"

	# Assemble the df

	data = pd.DataFrame({"":time_labels,"Tests conducted":totals,"Positive results":positives,"Positive rate":pos_rates})

	return data

def interjection(df):
	# Check for interjection
	for n in [-1,-2]:
		interjection = df[exp].iloc[n]
		if not pd.isnull(interjection):
			return dbc.Col([dbc.Jumbotron([html.Div([f"*{interjection}"],style={"fontSize":"130%"})])])

