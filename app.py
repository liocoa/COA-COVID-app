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
import dash_table

import plots


#Campus population
POP = plots.POP


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

df = pd.read_csv('data/dummyData2.csv')


# Perform calculations

df = plots.calculate(df)

# Prep figures

table_data = plots.make_table_df(df)
cases_timeseries = plots.timeseries(df)
test_rect = plots.testing_rectangle(df)


colors = {
    'header_bg': 'darkgrey'
}


# pass to graph objects to make them static
config = {'staticPlot': True}


app.layout = html.Div([
	# A header
	dbc.Navbar([
		dbc.Row([
			# COA logo
			dbc.Col(html.Img(
						id="COA-seal",
						src=app.get_asset_url('coa-seal.jpg'),
						style={
							"height":"100px",
							"width":"auto"
						}),
			width=3
			),
			# A title
			dbc.Col(html.H1("COA COVID dashboard layout"),width=9)
			])
		],
		color="primary"
		),

	html.Br(),

	# The main content
	dbc.Container(
	    [
	        dbc.Row(
	        	[
	        		dbc.Col(
	        			html.Div(
		        			dcc.Graph(
		        				id="timeseries-graph",
		        				figure=cases_timeseries,
		        				config=config
		        				)
		        			),
	    			),
	        		dbc.Col(
	        			html.Div(
	        				id="case_number",
	        				children=[dbc.Jumbotron([
	        					html.H3("Active cases",style={"textAlign":"center"}),
	        					html.H1(str(df["active_cases"].iloc[-1]),style={"textAlign":"center"})
	        				])
	        				]
	        				#style={"backgroundColor":"brown"}
	        				),
	        			width=4
	        			)
	        	]
	        ),
	        html.Br(),
	        dbc.Row([
                


                dbc.Col([
                	html.Div([
                		dbc.Table.from_dataframe(table_data, striped=True, bordered=True, hover=False)
                	])
                ])
	         ]),
	        html.Br(),
	        dbc.Row(
	        	[
	        		dbc.Col(dcc.Graph(figure=plots.donut_isol(df),config=config)),
	        		dbc.Col([
	                	html.Div([
	                		dcc.Graph(id="test_rectangle",
	                			figure=test_rect,
	                			config=config)
	                		])
                	]),
                	dbc.Col(dcc.Graph(figure=plots.donut_quar(df),config=config)),
	        	]
	        )
	    ],
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)