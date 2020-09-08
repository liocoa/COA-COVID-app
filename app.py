# -*- coding: utf-8 -*-

# Run this locally with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import plots as p


#Campus population
POP = p.POP


app = dash.Dash(__name__)


# Actual data link: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5WH3RNN_pzZVH-emkww1ZaOP-3SfZfTYTjFjTuhLMm4v6rVWKIxCdT5lhnLZbqkr3ZyIvqa4j6dsi/pub?gid=74385221&single=true&output=csv'
# Dummy data for testing: 'https://tinyurl.com/y2z3ox8p'

# Don't publish until there's data in the actual data sheet.
# The app will break if it doesn't have data to draw from!


#COA_data_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS5WH3RNN_pzZVH-emkww1ZaOP-3SfZfTYTjFjTuhLMm4v6rVWKIxCdT5lhnLZbqkr3ZyIvqa4j6dsi/pub?gid=74385221&single=true&output=csv'
COA_data_url = 'https://tinyurl.com/y2z3ox8p'

df = pd.read_csv(COA_data_url)

df_maine = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRPtRRaID4XRBSnrzGomnTtUUkq5qsq5zj8fGpg5xse8ytsyFUVqAKKypYybVpsU5cHgIbY3BOiynOC/pub?gid=0&single=true&output=csv')


# Perform calculations

df = p.calculate(df)

df_maine = p.maine_relevant_data(df_maine)





# Prep figures

table_data = p.reporting_table(df)
cases_timeseries = p.timeseries(df)
#test_rect = p.donut_total_tests(df)

# Get colors from plots file
colors = p.colors

# Get the most recent update timestamp
updated = df["Timestamp"].iloc[-1]
updated = updated.split(" ")[0]





# pass to graph objects to make them static
config = {'staticPlot': True}


app.layout = html.Div([

	# The main layout
	dbc.Container([

		# Updated date

		dbc.Row([
			dbc.Col([
				html.Div([f"Updated {updated}"],style={"textAlign":"center"})
			])
		]),

		html.Br(),
		
		# First row: the table

		dbc.Row([
    		
    		dbc.Col([
            	html.Div([
            		dbc.Table.from_dataframe(table_data, striped=True, bordered=True, hover=False)
            	])
            ])
        	
	    ]),

		html.Br(),

		# Second row: active and recovered numbers

        dbc.Row([

			dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H2("Active cases",style={"textAlign":"center"}),
						html.H1(str(df[p.active].iloc[-1]),style={"textAlign":"center"})
					]),
    			),
    		sm=6
    		
    		),

    		dbc.Col(
    			html.Div(
					dbc.Jumbotron([
						html.H2("Recovered cases",style={"textAlign":"center"}),
						html.H1(str(df[p.recovered].sum()),style={"textAlign":"center"})
					]),
    			),
    		sm=6

    		)


        ]),


        html.Br(),

        # Third row: timeseries

        dbc.Row([
        	dbc.Col(
    			dcc.Graph(
    				id="timeseries-graph",
    				figure=cases_timeseries,
    				config=config
    			),
    		width=12
			)
        ]),

        # Fourth row: donuts

        dbc.Row([

            dbc.Col(p.donut_isol(df),sm=6),

    		dbc.Col(p.donut_quar(df),sm=6)

    		


        ]),


        html.Br(),

        # Fifth row: county and state numbers

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

        # Optional sixth row: interjection

        dbc.Row([
        	p.interjection(df)
        ])
        
	],
	# main layout container kwargs
	fluid=True


	),

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
						html.P("Isolation: anyone testing positive for COVID-19 will be required to isolate until they are cleared by the COA COVID-19 health team"),
						html.P("Quarantine: anyone who has been in close contact with someone who tests positive for COVID-19 will be required to quarantine until cleared by the COA COVID-19 health team"),
						# html.P("Overall positive rate: the percentage of all tests done on COA community members that have returned positive results"),
						html.P(["State and county data: from the Cases by County Table on ",html.A("maine.gov",href='https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus/data.shtml')]),
						html.P(["COA data: ",html.A("download here",href=COA_data_url),])
					])
				)
			]),

			html.Br()

		],
		fluid=True
		)
	],
	style={"backgroundColor":colors["COAgreen"]}
	)

])

if __name__ == '__main__':
    app.run_server(debug=True)