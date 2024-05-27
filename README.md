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
For get the data I create this function.

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
    
