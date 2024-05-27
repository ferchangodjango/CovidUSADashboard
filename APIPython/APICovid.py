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
    
