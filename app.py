# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

df = pd.read_csv('data/dummyData1.csv')

fig1 = px.line(df,x="date",y="active_cases")
fig2 = px.line(df,x="date",y="current_quar")
fig3 = px.scatter(df,x="positive",y="quar_in")






app.layout = html.Div([
	# A header



	# The main content
	dbc.Container(
	    [
	    	dbc.Row(dbc.Col(html.H1("This is a title!"))),
	        dbc.Row(
	        	[
	        		dbc.Col(dcc.Graph(figure=fig1),width=6),
	        		dbc.Col(dcc.Graph(figure=fig2),width=6)
	        	]
	        ),
	        html.Br(),
	        dbc.Row(
	            [
	                dbc.Col(dcc.Graph(figure=fig3))
	            ]
	        ),
	    ],
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)