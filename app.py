# -*- coding: utf-8 -*-

# Run this locally with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# online at 
# coa-covid.herokuapp.com and
# https://coa.edu/news/covid-19/covid-19-dashboard/

import os

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

server = app.server



############################################################################

# Access COA data directly through Google Drive API
import io
import os

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

import googleapiclient.discovery
from googleapiclient.http import MediaIoBaseDownload

drive_service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)

file_id = '1lFYO6N31Vy1P52HS-1ttu1sJig65Wwdtnbgcmy7RRwI'
request = drive_service.files().export_media(fileId=file_id,
                                             mimeType='text/csv').execute()

df = pd.read_csv(io.BytesIO(request))

##################################################################



df_maine = "argh"





# Perform calculations

df = p.calculate(df)

df_maine = p.maine_relevant_data(df_maine)




# Get colors from plots file
colors = p.colors

# Get the most recent update timestamp
updated = df["Timestamp"].iloc[-1]
updated = updated.split(" ")[0]





# pass to graph objects to make them static
config = {'staticPlot': True}


app.layout = html.Div([
	# Header
	html.Header(html.Div(),style={"backgroundColor":colors["COAgreen"],"height":"50px"}),



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
            		dbc.Table.from_dataframe(p.reporting_table(df), striped=True, bordered=True, hover=False)
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




        # Third row: timeseries

        dbc.Row([
        	dbc.Col([
    			p.timeseries(df)
    		],
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
						# html.P(["COA data: ",html.A("download here",href=COA_data_url),])
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