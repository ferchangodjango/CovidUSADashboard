# Dashboard from Covid.

In this Dash Board you can see the follow:

![image](https://github.com/ferchangodjango/CovidUSADashboard/assets/68520215/2f97f4da-699c-40b7-a475-deec690523f2)

This a dinamic DashBoard, and you can interact with the dashboard.

## This readme have 3 Parts.
1. API and requests.
2. Dinamic Graphs (Java Script Callbacks).
3. Functions and References.

Enjoy!!
## 1. API and requests.

The data from this work is in this URL :https://api.covidtracking.com

### 1.1. connection
For get the data I create a class called managmenteAPI(), this class have a 
classmethods for create the connection with a external API(connection method) or internal connection.

#### Parameters
This function need the follow parameters:
url: Is a url from the end point of the API, for get the information.
columnName: Is a specific columns from the JSON, if the JSON don´t have the data than you want in a specific column, don´t
put anything.
#### Returns
This function return a DataFrame with the information.

#### Code
```python
import requests
import pandas as pd

class managmenteAPI():
    @classmethod
    def conection(self,url,columnName=None):
        """This function get the information about any url, 
        and return a DataFrame with this data"""
        data=requests.get(url)
        if data.status_code==200:
            data=data.json()
            if columnName==None:
                DataFrame=pd.json_normalize(data)
            else:
                DataFrame=pd.json_normalize(data[columnName])
        return DataFrame
```
This function extracted the information and create a Data Frame with that information

The URL for get the information is the follow:
```python
urlCovid={
    "covidtraqcking":"https://api.covidtracking.com/v1/us/daily.json",
    "states":"https://api.covidtracking.com/v1/states/info.json",
    "covidtraqckingHistoric":"https://api.covidtracking.com/v1/states/daily.json"
}
```
### 1.2. Internal connection

For the principle that say "a function have to do one thing, and only one thing", I  thought, than each view
give me a Graph or a DataFrame, and create eache API for get one functionality, for can connect this API with my
dashboard, I create a internalConnection function

#### Parameters
This function need the follow parameters:
url: Is a url from the end point of the API, for get the information.

#### Returns
This function return a JSON with the information.

#### Code
```python
    @classmethod
    def internalConnection(self,url):
        """This function get the information about any url, 
        and return a JSON"""
    
        MapaData=requests.get(url)
        if MapaData.status_code==200:
            MapaData=MapaData.json()
```


## 2. Dinamic Graphs (Java Script Callbacks).
For this part you need to know anything about Java script, only the basic.

We start with the Map Graph
For this section you need to import this
```python
from bokeh.layouts import column
from bokeh.models import LogColorMapper,ColumnDataSource,CustomJS,Range1d,LinearAxis,HoverTool,NumeralTickFormatter,Slider,RangeTool
from bokeh.models.widgets import Select
from bokeh.plotting import figure
from bokeh.palettes import Turbo256
from bokeh.sampledata.us_states import data as states
```

Well remember than a Graph Map is only a graph to cordenetes (Lons and Lats).
For get the cordenates you can look up in bokeh.sampledata.
In this DashBoard, I used the USA cordenates for graph the USA Map, this information is in 
```python
from bokeh.sampledata.us_states import data as states
```
Well if you saw the us_states, you can saw a JSON with many kind of data, but we only need the cordenates, so 
we can extracted them with the follow code

```python
name_states=[state['name'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
states_xs=[state['lons'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
states_ys=[state['lats'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
#This is important geographic part, becouse we get a dataFrame wit all the cordenates
Geographic_data=dict(
    cordenate_x=states_xs,
    cordenate_y=states_ys,
    name=name_states,
)
```
The result is a dictionary with the cordanate lons, cordnates lats and names of this states.
Now we need other column for can graph, you can graph any value, and this work how a Pareto, mark each state wit a color,
and you can see a beauty Map, with a color scale.
for example, for demostrative excerice you can add a list about the numbers between 1 and 51(Than is the number of states than I have in the dictionary), and with this you have the follow code, with this dictionary we can do the graph.

```python
name_states=[state['name'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
states_xs=[state['lons'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
states_ys=[state['lats'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
Numbers_demostrative=[i for i in range(51)]
#This is important geographic part, becouse we get a dataFrame wit all the cordenates
Geographic_data=dict(
    cordenate_x=states_xs,
    cordenate_y=states_ys,
    name=name_states,
    rates=Numbers_demostrative
)
```
Before to pass to explain the function, you need to know the pallets, becouse this is the colors than you paint your graph,you can more information about the pallets in this link:https://docs.bokeh.org/en/latest/docs/reference/palettes.html#d3-palettes
Now its time to explain the MapDinamic Graph.

### 2.1 MapDinamic
#### Parameters
This function need the follow parameters:
DataFrame: Is a the data frame than we can create with the dictionay in the before section section.

```python
Geographic_data=dict(
    cordenate_x=states_xs,
    cordenate_y=states_ys,
    name=name_states,
    rates=Numbers_demostrative
)
DataFrame=pd.DataFrame(Geographic_data)
```
column_values: is the columns than indicate the kind of color, that need to paint.
palette: Is the kind of palette than you choice for you graph.
#### Returns
This function return a object bokehGraph, and for this bokeh graph you can get the resources for you embebed templates

#### Code
```python
def MapDinamic(DataFrame,column_values,palette,width=800,height=500,ranges=None):
    palette=tuple(reversed(palette))
    color_mapper=LogColorMapper(palette=palette)
    DataSources=ColumnDataSource(DataFrame)
    figure1=figure(
        title="USA States TEST",
        width=width,
        height=height,
        x_axis_location=None,
        y_axis_location=None,
        tooltips=[
            ("Name","@name"),
            (f"{column_values}",f"@{column_values}")])
    figure1.toolbar.autohide=True
    figure1.grid.grid_line_color=None
    figure1.hover.point_policy="follow_mouse"
    figure1.patches("cordenate_x","cordenate_y",
                    source=DataSources,
                    fill_color={"field":f"{column_values}",
                                "transform":color_mapper},
                    fill_alpha=0.6,
                    line_color="black",
                    line_width=0.5)
    if ranges==None:
        return figure1
    else:
        figure1.x_range=Range1d(ranges["lix1"],ranges["lsx2"])
        figure1.y_range=Range1d(ranges["liy1"],ranges["lsy2"])
        return figure1
```

### 2.2 Dinamic Pareto
#### Code
The dinamic Pareto have the base about a Pareto, check the reference:
but this have a javaScript code, I think than this do interesting this code, becouse we mixed code
python with Java Script
In this part firs we define a Slider element, for have a range of posibilities to choise,
```python
    number_slider = Slider(
        start=1,
        end=len(DataSourse.data[f"{column_index}"]),
        value=len(figure1.x_range.factors),
        title="Number of states",
    )
```
The second is define a CustomJS element, and this is the vicule to mixed the code,
this element have the args, than is the objects that is modify for the java scriot code, in this case
the target element is the Graph, called figure1, and the second element is the data, becouse the Java Script use the data
for can make changes in the graph, in this case the data is in DataSources, specific in the column_index.
And finally is the code, in this case only have two lines of code
```python
figure1.title.text = "Top " + this.value + " states from USA"; 
```
This line set the title name, in function about the value than the user choice in the selector, the value that is in the selector is getting through the comand "this.value".

```python
figure1.x_range.factors = DataSourse.slice(0,this.value);
```
This line set the range in the axis X, this set the ranges since 0 to  the value than the user choise in the selector,
and this values is getting throug the comand "this.value"
```python
    custom_js = CustomJS(
        args={  # the args parameter is a dictionary of the variables that will be accessible in the JavaScript code
            "figure1": figure1, 
            "DataSourse": DataSourse.data[f"{column_index}"],
        },
        code="""
        figure1.title.text = "Top " + this.value + " states from USA";  
        figure1.x_range.factors = DataSourse.slice(0,this.value);
        """,
        )
    number_slider.js_on_change("value", custom_js)
```

```python
def ParetoDinamicColors(DATA_FRAME,column_index,column_values,palette=Turbo256,width=500,height=500,initial=5):
    #Set the color
    palette=tuple(reversed(palette))
    SizeDataFrame=DATA_FRAME[column_values].count()
    TurboFitSize=[palette[i*4+30] for i in range(SizeDataFrame)]
    #Do pareto table.
    TOTAL=DATA_FRAME[column_values].sum()
    DATA_FRAME=DATA_FRAME.sort_values(by=column_values,ascending=False)
    DATA_FRAME['Porcentaje']=100*(DATA_FRAME[column_values]/TOTAL)
    DATA_FRAME['Porcentaje_acumulado']=DATA_FRAME['Porcentaje'].cumsum()
    DATA_FRAME['Color']=TurboFitSize
    
    #Set pareto table how the source of next graphs.
    DataSourse=ColumnDataSource(DATA_FRAME)
    
    #Create the figure called figure 1
    figure1=figure(
        x_range=DataSourse.data[f"{column_index}"][:initial],title=column_values,
        width=width,height=height,
        tools='reset,box_zoom',toolbar_location='below'
        )
    
    #General sets, how label´s name, color´s grid etc.
    figure1.xgrid.grid_line_color=None
    figure1.xaxis.axis_label=column_index
    figure1.xaxis.major_label_text_font_size='10px'
    figure1.yaxis.axis_label=column_values
    figure1.xgrid.grid_line_color=None
    figure1.ygrid.grid_line_alpha=0.7
    figure1.toolbar.autohide=True
    figure1.y_range.start = 0
    figure1.x_range.range_padding = 0.1
    figure1.xaxis.major_label_orientation = 1
    figure1.xgrid.grid_line_color = None
    figure1.yaxis.formatter = NumeralTickFormatter(format="0,0")  # format y-axis ticks
    
    # Create the seconde y axis for the % acumulate
    figure1.extra_y_ranges = {"y2": Range1d(start = 0, end = 110)}
    figure1.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    
    #Create the Graphs
    GRAPHBAR=figure1.vbar(
        x=column_index,top=column_values,
        width=0.9,fill_color='Color',
        line_color="#2E4053",source=DataSourse
        )
    GRAPHLINE=figure1.line(
        x=column_index,y='Porcentaje_acumulado',
        y_range_name='y2',source=DataSourse
        )
    GRAPHSCATTER=figure1.scatter(
        x=column_index,y='Porcentaje_acumulado',
        y_range_name='y2',source=DataSourse)
    
    #Create the hover for can show the values of graph
    hover=HoverTool(
        tooltips=[
            (column_index,'@'+column_values),
            ('% profit acumulete','@Porcentaje_acumulado'), 
            ('% profit','@Porcentaje')]
            )
    figure1.add_tools(hover)
    
    number_slider = Slider(
        start=1,
        end=len(DataSourse.data[f"{column_index}"]),
        value=len(figure1.x_range.factors),
        title="Number of states",
    )

    custom_js = CustomJS(
        args={  # the args parameter is a dictionary of the variables that will be accessible in the JavaScript code
            "figure1": figure1, 
            "DataSourse": DataSourse.data[f"{column_index}"],
        },
        code="""
        figure1.title.text = "Top " + this.value + " states from USA";  
        figure1.x_range.factors = DataSourse.slice(0,this.value);
        """,
        )
    number_slider.js_on_change("value", custom_js)
    dinamicGraph = column([number_slider, figure1], sizing_mode="stretch_width")
    
    return dinamicGraph

```
