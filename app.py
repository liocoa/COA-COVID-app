# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


#Campus population
POP = 350


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

df = pd.read_csv('data/dummyData1.csv')


# Perform calculations


# Calculate current isolations
current_isol = np.zeros(len(df)).astype(int)
current_isol[0] = df["isol_in"][0]
for i in range(len(df)-1):
    current_isol[i+1] = current_isol[i] + df["isol_in"][i+1] - df["isol_out"][i+1]
df["current_isol"] = current_isol


# define figures
def donut_isol(df):
    current_isol_val = df["current_isol"].iloc[-1]
    isol_pie_labels = ["In isolation","unisolated"]
    isol_pie_values = [current_isol_val,POP-current_isol_val]

    fig = go.Figure(data=[go.Pie(labels=isol_pie_labels, values=isol_pie_values, hole=0.6)])
    return fig


fig1 = px.line(df,x="date",y="active_cases")
fig2 = px.line(df,x="date",y="current_quar")
fig3 = px.scatter(df,x="positive",y="quar_in")


colors = {
    'header_bg': 'darkgrey'
}



app.layout = html.Div([
	# A header
	dbc.Container([
		dbc.Row([
			# COA logo
			dbc.Col(html.Img(
						id="COA-seal",
						src=app.get_asset_url('coa-seal.jpg'),
						style={
							"height":"60px",
							"width":"auto"
						}),
				width=1),
			# A title
			dbc.Col(html.H1("COA COVID dashboard layout"))
			])
		]),


	# The main content
	dbc.Container(
	    [
	        dbc.Row(
	        	[
	        		dbc.Col(
	        			dcc.Graph(
	        				id="timeseries-graph",
	        				figure=fig1),
	        			width=9),
	        		dbc.Col(
	        			html.Div(
	        				id="case_number",
	        				children=[
	        					html.Div("Active cases"),
	        					html.Div(str(df["active_cases"].iloc[-1]))
	        				],
	        				style={"backgroundColor":"brown"}
	        				)
	        			)
	        	]
	        ),
	        html.Br(),
	        dbc.Row(
	            [
	                dbc.Col(dcc.Graph(figure=fig3))
	            ]
	        ),
	        html.Br(),
	        dbc.Row(
	        	[
	        		dbc.Col(dcc.Graph(figure=donut_isol(df))),
	        		dbc.Col(dcc.Graph(figure=donut_isol(df)))
	        	]
	        )
	    ],
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)