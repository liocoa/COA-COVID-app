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

import plots as p


#Campus population
POP = p.POP


app = dash.Dash(__name__)

df = pd.read_csv('https://tinyurl.com/y2z3ox8p')


# Perform calculations

df = p.calculate(df)

# Prep figures

table_data = p.make_table_df(df)
cases_timeseries = p.timeseries(df)
test_rect = p.donut_total_tests(df)

colors = {"COAblue":"#003399","COAgreen":"#669999"}




# pass to graph objects to make them static
config = {'staticPlot': True}


app.layout = html.Div([
	# HEADER
	dbc.Navbar([
		dbc.Row([
			# COA logo
			dbc.Col(
				html.Img(
					id="COA-seal",
					src=app.get_asset_url('coa_seal_transparency.png'),
					style={
						"height":"100px",
						"width":"auto"
					}
				),
				width=3
			),
			# A title
			dbc.Col(html.H1("COA COVID Tracker"),width=9)
		])
	],
	color="grey"
	),

	html.Br(),

	# The main layout
	dbc.Container([
        dbc.Row([
    		dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H3("Active cases",style={"textAlign":"center"}),
						html.H1(str(df[p.active].iloc[-1]),style={"textAlign":"center"})
					]),
    			),
    		width=4
    		),

    		dbc.Col(
    			dcc.Graph(
    				id="timeseries-graph",
    				figure=cases_timeseries,
    				config=config
    			)
			)

    		

    		

        ]),

		html.Br(),

        dbc.Row([
    		
    		dbc.Col([
            	html.Div([
            		dbc.Table.from_dataframe(table_data, striped=True, bordered=True, hover=False)
            	])
            ])
        	
	    ]),


        html.Br(),

        dbc.Row([
            

            dbc.Col(dcc.Graph(figure=test_rect,config=config),width=4),

            dbc.Col(dcc.Graph(figure=p.donut_isol(df),config=config)),

    		dbc.Col(dcc.Graph(figure=p.donut_quar(df),config=config))

         ])

        
	])
])

if __name__ == '__main__':
    app.run_server(debug=True)