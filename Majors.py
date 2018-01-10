# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 12:33:21 2017

@author: Taranpreet

Code for app for under graduate majors
"""
import pandas as pd
deg = pd.read_csv("deg.csv")



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
from bokeh.layouts import row 
# Create ColumnDataSource: source
source = ColumnDataSource(data={
    'x' : deg.startSalary,
    'y' : deg.index,
    'z' : deg.midSalary
})

# Create a new plot: plot
p = figure(x_axis_label='Salary in US $',plot_height=800, y_axis_label='Major')

p.title.text = "Salaries by Majors"
p.title.align = "center"
p.title.text_color = "blue"
p.title.text_font_size = "20px"



# Add a circle glyph to the figure p
p.circle('x', 'y',legend="Selcted salary",source=source)
p.circle('z', 'y',color='orange',legend="Mid career salary",source=source)
p.yaxis.ticker=deg.index
p.legend.location = "bottom_right"

#labelling y axis
label_dict = {}
for i, s in enumerate(deg.Major):
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
            'x' : deg.startSalary,
            'y' : deg.index,
            'z' : deg.midSalary
        }
    elif new == '10 %ile Salary': 
        source.data = {
            'x' : deg.mid10,
            'y' : deg.index,
            'z' : deg.midSalary
        }   
    elif new == '25 %ile Salary': 
        source.data = {
            'x' : deg.mid25,
            'y' : deg.index,
            'z' : deg.midSalary
        }  
    elif new == '75 %ile Salary': 
        source.data = {
            'x' : deg.mid75,
            'y' : deg.index,
            'z' : deg.midSalary
        }    
                  
    
    else:
        source.data = {
            'x' : deg.mid90,
            'y' : deg.index,
            'z' : deg.midSalary
        }

# Create a dropdown Select widget: select    
select = Select(title="Select salary type ",
                options=['Starting Salary','10 %ile Salary','25 %ile Salary', 
                         '75 %ile Salary','90 %ile Salary',], 
                         value='Starting Salary')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)




'''

#Plot 2


coll=pd.read_csv("coll.csv")


source1 = ColumnDataSource(data={
    'x' : coll.Type,
    'y' : coll.midSalary
})    
###
      
# Create a new plot: plot
#p1 = figure(x_axis_label='College Type', y_axis_label='Salary')
p1 = Bar(coll,'Type', values='midSalary')


p1.title.text = "Salaries by type of institution"
p1.title.align = "center"
p1.title.text_color = "blue"
p1.title.text_font_size = "20px"


#p1 = Bar('x', values='y',source=source1)

#output_file("bar.html")
#show(p)
###

# Define a callback function: update_plot
def update_plot1(attr, old, new):
    # If the new Selection is 'female_literacy', update 'y' to female_literacy
    if new == 'Starting Salary': 
        source1.data = {
            'x' : coll.Type,
            'y' : coll.startSalary
           
        }
   
    elif new == '25 %ile Salary': 
          source1.data = {
            'x' : coll.Type,
            'y' : coll.mid25
           
        }
    elif new == '75 %ile Salary': 
            source1.data = {
            'x' : coll.Type,
            'y' : coll.mid75
           
        }
                  
    # Else, update 'y' to population
    else:
         source1.data = {
            'x' : coll.Type,
            'y' : coll.midSalary
           
        }

# Create a dropdown Select widget: select    
select1 = Select(title="Select salary type ",
                options=['Starting Salary','25 %ile Salary', 
                         '75 %ile Salary','Median Salary'], 
                         value='Starting Salary')

# Attach the update_plot callback to the 'value' property of select
select1.on_change('value', update_plot1)




reg=pd.read_csv("reg.csv")



source1 = ColumnDataSource(data={
    'x' : coll.Type,
    'y' : coll.midSalary
})    
###
       
# Create a new plot: plot
#p1 = figure(x_axis_label='College Type', y_axis_label='Salary')
p2 = Bar(reg,'Region', values='midSalary')


'''

############
# Create layout and add to current document
layout = row(select,p)
curdoc().add_root(layout)
