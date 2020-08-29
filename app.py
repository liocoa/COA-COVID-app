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
			dbc.Col(html.H1("COA COVID dashboard ALPHA"))
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
	    ],
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)