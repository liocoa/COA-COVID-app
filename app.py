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
    percent_isol = current_isol_val/POP*100
    isol_pie_values = [current_isol_val,POP-current_isol_val]

    fig = go.Figure(data=[go.Pie(values=isol_pie_values, hole=0.5)])
    
    # Title, suppress legend
    fig.update_layout(title={"text":" Current Isolations","x":0.5,"xanchor":"center"}, showlegend=False)
    # Trace labels and hover info
    fig.update_traces(textinfo="none",hoverinfo='none')
    # Center data
    fig.add_annotation(text=f"{percent_isol:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)
    # Fine print
    fine_print = "*percent of total campus program participants"
    fig.add_annotation(text=fine_print, x=0.5, y=1.1, showarrow=False)
    
    return fig

def donut_quar(df):
    current_quar_val = df["current_quar"].iloc[-1]
    percent_quar = current_quar_val/POP*100
    quar_pie_values = [current_quar_val,POP-current_quar_val]

    fig = go.Figure(data=[go.Pie(values=quar_pie_values, hole=0.5)])
    
    # Title, suppress legend
    fig.update_layout(title={"text":"Current Quarantines","x":0.5,"xanchor":"center"}, showlegend=False)
    # Trace labels and hover info
    fig.update_traces(textinfo="none",hoverinfo='none')
    # Center data
    fig.add_annotation(text=f"{percent_quar:.1f}%", x=0.5, y=0.5, font_size=20, showarrow=False)
    # Fine print
    fine_print = "*percent of on-campus housing residents"
    fig.add_annotation(text=fine_print, x=0.5, y=1.1, showarrow=False)
    
    return fig

def make_table_df(df):
	labels = ["Total tested:", "Total negative:", "Positive rate:"]
	current_vals = [df["tested"].iloc[-1],
	                df["negative"].iloc[-1]]
	previous_vals = [df["tested"].iloc[-2],
	                 df["negative"].iloc[-2]]
	since_vals = [df["tested"].sum(),
	              df["negative"].sum()]

	for vals in [current_vals,previous_vals,since_vals]:
	    pos_rate = (vals[0]-vals[1])/vals[0]*100
	    vals.append(f"{pos_rate:.1f}%")

	data = pd.DataFrame({"":labels,"This week":current_vals,
	                   "Last week":previous_vals,f"Since {df['date'].iloc[0]}":since_vals})
	return data

def testing_rectangle(df):
	# A graph for total + and - from campus testing

	# Make a square whose area is equal to the number of tests conducted
	total_tests = df["tested"].sum()
	test_side_length = np.sqrt(total_tests)

	# Make a square whose area is equal to the number of positive results
	total_pos = df["positive"].sum()
	pos_side_length = np.sqrt(total_pos)

	# Make the graph
	fig = go.Figure()

	# Set axis properties (get rid of gridlines and axis scales)
	fig.update_xaxes(range=[-0.1*test_side_length, 1.1*test_side_length], showgrid=False, zeroline=False, visible=False)
	fig.update_yaxes(range=[-0.1*test_side_length, 1.1*test_side_length], showgrid=False, zeroline=False, visible=False)

	# Other layout
	fig.update_layout(title="Proportion of total tests that were positive")

	# A shape for tests
	fig.add_shape(type="rect",
	             x0=0,
	             y0=0,
	             x1=test_side_length,
	             y1=test_side_length,
	             fillcolor="lightskyblue")

	# A shape for positives
	fig.add_shape(type="rect",
	             x0=0,
	             y0=0,
	             x1=pos_side_length,
	             y1=pos_side_length,
	             fillcolor="firebrick")

	return fig



table_data = make_table_df(df)
cases_timeseries = px.line(df,x="date",y="active_cases")
test_rect = testing_rectangle(df)




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
	        			html.Div(
		        			dcc.Graph(
		        				id="timeseries-graph",
		        				figure=cases_timeseries
		        				)
		        			),
	    			),
	        		dbc.Col(
	        			html.Div(
	        				id="case_number",
	        				children=[
	        					html.Div("Active cases",style={"textAlign":"center"}),
	        					html.Div(str(df["active_cases"].iloc[-1]),style={"textAlign":"center"})
	        				],
	        				style={"backgroundColor":"brown"}
	        				),
	        			width=4
	        			)
	        	]
	        ),
	        html.Br(),
	        dbc.Row([
                dbc.Col([
                	html.Div([
                		dcc.Graph(id="test_rectangle",
                			figure=test_rect)
                		])
                	]),


                dbc.Col([
                	html.Div([
                		dash_table.DataTable(
                			id="Table",
                			columns=[{"name": i, "id": i} for i in table_data.columns],
    						data=table_data.to_dict('records'),
    						style_cell={"color":"black"},
    						style_as_list_view=True
                		)
                	])
                ])
	         ]),
	        html.Br(),
	        dbc.Row(
	        	[
	        		dbc.Col(dcc.Graph(figure=donut_isol(df))),
	        		dbc.Col(dcc.Graph(figure=donut_quar(df)))
	        	]
	        )
	    ],
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)