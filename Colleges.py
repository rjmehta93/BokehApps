# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:25:34 2017

@author: Taranpreet

Code for colleges.py
"""

# Perform necessary imports
import pandas as pd
coll = pd.read_csv("coll.csv")



# Perform necessary imports
from bokeh.plotting import figure

# Import output_file and show from bokeh.io
#from bokeh.io import output_file, show 
#from bokeh.charts import Bar#, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import FuncTickFormatter, NumeralTickFormatter

from bokeh.models import Title

from bokeh.models import Select
from bokeh.io import curdoc
from bokeh.layouts import column 
# Create ColumnDataSource: source
source = ColumnDataSource(data={
    'x' : coll.startSalary,
    'y' : coll.index,
    'z' : coll.midSalary
})

# Create a new plot: plot
p = figure(x_axis_label='Salary in US $',
           y_axis_label='Institution',plot_height=3500,plot_width=800)

p.title.text = "Salaries by Institutions"
p.title.align = "center"
p.title.text_color = "blue"
p.title.text_font_size = "20px"



# Add a circle glyph to the figure p
p.circle('x', 'y',legend="Selcted salary",source=source)
p.circle('z', 'y',color='orange',legend="Mid career salary",source=source)
p.yaxis.ticker=coll.index
p.legend.location = "top_left"

label_dict = {}
for i, s in enumerate(coll.School):
    label_dict[i] = s

p.yaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)

hover = HoverTool(tooltips=[
                            ('Selected Salary','@x'),
                            ('Mid career Salary','@z')])
                            


# Add the HoverTool object to figure p
p.add_tools(hover)


p.xaxis.formatter=NumeralTickFormatter(format="0,000")
#output_file("bar.html")
#show(p)
p.add_layout(Title(text="Comaprison with median salary",
                   align="center",text_color="blue"), "below")



# Define a callback function: update_plot
def update_plot(attr, old, new):
   
    if new == 'Starting Salary': 
        source.data = {
            'x' : coll.startSalary,
            'y' : coll.index,
            'z' : coll.midSalary
        }
    elif new == '10 %ile Salary': 
        source.data = {
            'x' : coll.mid10,
            'y' : coll.index,
            'z' : coll.midSalary
        }   
    elif new == '25 %ile Salary': 
        source.data = {
            'x' : coll.mid25,
            'y' : coll.index,
            'z' : coll.midSalary
        }  
    elif new == '75 %ile Salary': 
        source.data = {
            'x' : coll.mid75,
            'y' : coll.index,
            'z' : coll.midSalary
        }    
                  
    # Else, update 'y' to population
    else:
        source.data = {
            'x' : coll.mid90,
            'y' : coll.index,
            'z' : coll.midSalary
        }

# Create a dropdown Select widget: select    
select = Select(title="Select salary type ",
                options=['Starting Salary','10 %ile Salary','25 %ile Salary', 
                         '75 %ile Salary','90 %ile Salary',], 
                         value='Starting Salary')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

layout = column(select,p)
curdoc().add_root(layout)