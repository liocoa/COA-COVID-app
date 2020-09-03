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

df_maine = pd.read_csv('https://tinyurl.com/y45pf56k')


# Perform calculations

df = p.calculate(df)

df_maine = p.maine_relevant_data(df_maine)


# Prep figures

table_data = p.reporting_table(df)
cases_timeseries = p.timeseries(df)
test_rect = p.donut_total_tests(df)

colors = p.colors




# pass to graph objects to make them static
config = {'staticPlot': True}


app.layout = html.Div([
	# HEADER
	html.Header([
		dbc.Container([

			html.Br(),

			dbc.Row([

				# COA logo
				dbc.Col(
					html.Img(
						id="COA-seal",
						src=app.get_asset_url('coa_seal_transparency.png'),
						style={
							"height":"75px",
							"width":"auto"
						}
					),
					width=1
				),
				# A title
				dbc.Col(html.H1("COA COVID-19 Dashboard"))
			]),

			html.Br()

		])
	],
	style={"backgroundColor":colors["COAgreen"]}
	),

	# End header

	html.Br(),

	# The main layout
	dbc.Container([
		
		# First row

		dbc.Row([
    		
    		dbc.Col([
            	html.Div([
            		dbc.Table.from_dataframe(table_data, striped=True, bordered=True, hover=False)
            	])
            ])
        	
	    ]),

		html.Br(),

		# Second row

        dbc.Row([

    		dbc.Col(
    			dcc.Graph(
    				id="timeseries-graph",
    				figure=cases_timeseries,
    				config=config
    			),
    		width=8
			),

			dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H2("Active cases",style={"textAlign":"center"}),
						html.H1(str(df[p.active].iloc[-1]),style={"textAlign":"center"})
					]),
    			),
    		width=4
    		)


        ]),


        html.Br(),

        # Third row

        dbc.Row([

            dbc.Col(dcc.Graph(figure=p.donut_isol(df),config=config),width=4),

    		dbc.Col(dcc.Graph(figure=p.donut_quar(df),config=config),width=4),

    		dbc.Col(dcc.Graph(figure=test_rect,config=config),width=4)

        ]),



        # Fourth row

        dbc.Row([
        	dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H2("Hancock County",style={"textAlign":"center"}),
						html.Div([f"Total cases: {df_maine.loc[0,'CASES']}"],style={"textAlign":"center","fontSize":"150%"}),
						html.Div([f"Total recovered: {df_maine.loc[0,'RECOVERIES']}"],style={"textAlign":"center","fontSize":"150%"}),
						html.Div([f"Cases per 10k people: {df_maine.loc[0,'PERCAP']:.1f}"],style={"textAlign":"center","fontSize":"150%"})

					]),
    			),
    		),
    		dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H2("State of Maine",style={"textAlign":"center"}),
						html.Div([f"Total cases: {df_maine.loc[1,'CASES']}"],style={"textAlign":"center","fontSize":"150%"}),
						html.Div([f"Total recovered: {df_maine.loc[1,'RECOVERIES']}"],style={"textAlign":"center","fontSize":"150%"}),
						html.Div([f"Cases per 10k people: {df_maine.loc[1,'PERCAP']:.1f}"],style={"textAlign":"center","fontSize":"150%"})
					]),
    			),
    		)
        ]),
        
	]),

	# End main layout.

	html.Br(),

	# Footer

	html.Footer([
		dbc.Container([

			html.Br(),

			dbc.Row([
				dbc.Col(
					html.Div([
						html.P("Active cases: the number of COA community members participating in the campus program who have COVID-19"),
						html.P("Isolations: anyone testing positive for COVID-19 will be placed in isolation until they receive a negative test result or are cleared by the COA COVID health team"),
						html.P("Quarantines: anyone who shows symptoms or has been in close contact with someone who tests positive for COVID-19 will be asked to quarantine at home until cleared by the COA COVID health team"),
						html.P("Overall positive rate: the percentage of all tests done on COA community members that have returned positive results"),
						html.P(["State and county data: from the Cases by County Table on ",html.A("maine.gov",href='https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus/data.shtml')]),
						html.P(["COA data: download at ",html.A("TEST LINK DO NOT PUBLISH ME",href='https://tinyurl.com/y2z3ox8p'),])
					])
				)
			]),

			html.Br()

		])
	],
	style={"backgroundColor":colors["COAgreen"]}
	)

])

if __name__ == '__main__':
    app.run_server(debug=True)