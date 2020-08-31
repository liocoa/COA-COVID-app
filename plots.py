# -*- coding: utf-8 -*-

# Importable module for making the more complex plots.
# I just prefer to have these in a separate place to avoid clutter.

def donut_isol(df):
    current_isol_val = df["current_isol"].iloc[-1]
    isol_pie_labels = ["In isolation","unisolated"]
    isol_pie_values = [current_isol_val,POP-current_isol_val]

    fig = go.Figure(data=[go.Pie(labels=isol_pie_labels, values=isol_pie_values, hole=0.6)])
    return fig