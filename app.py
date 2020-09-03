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

df_maine = p.maine_current(df_maine)

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
				dbc.Col(html.H1("COA COVID-19 Tracker",style={"verticalAlign":"bottom"}))
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
						html.H3("Active cases",style={"textAlign":"center"}),
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

        html.Br(),

        # Fourth row

        dbc.Row([
        	dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H3("Current Hancock county cases",style={"textAlign":"center"}),
						html.H1(df_maine[df_maine["PATIENT_COUNTY"]=="Hancock"]["CURRENT"],style={"textAlign":"center"})
					]),
    			),
    		),
    		dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H3("Current Maine state cases",style={"textAlign":"center"}),
						html.H1(df_maine["CURRENT"].sum(),style={"textAlign":"center"})
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
						html.P("Active cases: The number of active cases is the number of COA community members who have COVID-19."),
						html.P("Isolations: The isolation rate is the percent of COA community members in isolation (at the COA isolation facility, in the hospital, or isolated at home) as of the end date of this reporting period. Anyone who tests positive for COVID will be isolated until they receive a negative test result."),
						html.P("Quarantines: The quarantine rate is the percent of COA community members in quarantine (either on or off campus) as of the end date of this reporting period. Anyone who shows symptoms or has had contact with a person who has tested positive for COVID will be required to quarantine themselves until they receive a negative test result."),
						html.P("Overall positive rate: The overall positive rate is the percent of all tests done on COA community members (to our knowledge) that have returned positive results.")
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