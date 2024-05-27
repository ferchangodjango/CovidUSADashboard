from flask import Flask,request,render_template,redirect,url_for,flash,jsonify

#Config from the app
from config import externalObject
#Login
from flask_login import LoginManager,login_required,login_user,logout_user
from Models.Models import ModelUser
from Models.Entities.Users import User
#Conection and manage db
from flask_mysqldb import MySQL
from DB.ManageResources import ManageResources
#Scurity forms
from flask_wtf.csrf import CSRFProtect
from forms.forms import Forms
#Import Api managment
from APIPython.APICovid import managmenteAPI
from APIPython.urlCovid import urlCovid
from ManagmentTime.managmentTime import apply_scalars
import pandas as pd
#Import graphs
from graphs.dinamicGraphs import DinamicSeriesTime,ParetoDinamic,ParetoDinamicColors,MapDinamic
#Import cordenates from the states
from bokeh.sampledata.us_states import data as states
#Import the palette 
from bokeh.palettes import YlOrRd9 as palette
from bokeh.palettes import Turbo256
from bokeh.io import curdoc
#Eraser
import requests

app=Flask(__name__)
db=MySQL(app)
csrf=CSRFProtect(app)

"""______Start a standart session______"""
sessionManager=LoginManager(app)


@sessionManager.user_loader
def getByID(ID):
    """This is a standard session, than you know how to create it
    This function is for verify and manage the seccion"""
    return ModelUser.idUser(db,ID)

@app.route('/')
def index():
    """This is a standard session, than you know how to create it
    This function redirect to login, for login in the session"""
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    """This is a standard session, than you know how to create it
        This function validate the user from get a login"""
    if request.method=='POST':
        user=User(None,request.form['username'],request.form['password'])
        loggedUser=ModelUser.loggedUser(db,user)
        if loggedUser!=None:
            if loggedUser.password:
                login_user(loggedUser)
                return(redirect(url_for('home')))
            else:
                flash("Incorrect password")
                return render_template('login.html')
        else:
            flash("User not found")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """This is a standard session, than you know how to create it
    This function logout the session and return the page for login the
    session again"""
    logout_user()
    return redirect(url_for('login'))

"""______End a standart session______"""


"""______Start the CRUD______"""

@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    """This function return a form template with four buttons,
    the button for insert a new employeed, the button for delete an existent employeed,
    the button for update the data about any employeed"""
    formAPI=Forms()
    if request.method=='POST' and formAPI.validate:
        return render_template('CRUD/formularioAll.html',form=formAPI)
    else:
        return render_template('CRUD/formularioAll.html',form=formAPI)
    

"""______________Start the back end of the aplication_______________________"""

@app.route('/GeneratorData',methods=['GET'])
def GeneratorData():

    #__________Begin Get the dataframe master________
    
    # Define the URL
    traqckingUrl=urlCovid['covidtraqckingHistoric']
    statesUrl=urlCovid['states']
    
    # Get the data( all the data and row data)
    TraqckingCovidDataFrame=managmenteAPI.conection(traqckingUrl)
    statesData=managmenteAPI.conection(statesUrl)

    #Set the date
    TraqckingCovidDataFrame['date']=pd.to_datetime(TraqckingCovidDataFrame.date,format='%Y%m%d')
    TraqckingCovidDataFrame=apply_scalars(TraqckingCovidDataFrame,'date',year=True, month=True, week=True, shift=False)
    
    #Rename and transform a kind of data.
    statesData=statesData.rename(columns={'fips':'states'})
    statesData.states=statesData.states.astype('int64')

    # Merge the data
    OverallTraqckingCovid=TraqckingCovidDataFrame.merge(statesData,on='state')
    DictOverallTraqckingCovid=OverallTraqckingCovid.to_dict()
    
    
    return jsonify({'DATA':DictOverallTraqckingCovid})

@app.route('/SeriesTimeData', methods=['GET'])
def SeriesTimeData():
    #__________Begin Get the dataframe master________
    
    # Define the URL
    traqckingUrl=urlCovid['covidtraqckingHistoric']
    statesUrl=urlCovid['states']
    
    # Get the data( all the data and row data)
    TraqckingCovidDataFrame=managmenteAPI.conection(traqckingUrl)
    statesData=managmenteAPI.conection(statesUrl)

    #Set the date
    TraqckingCovidDataFrame['date']=pd.to_datetime(TraqckingCovidDataFrame.date,format='%Y%m%d')
    TraqckingCovidDataFrame=apply_scalars(TraqckingCovidDataFrame,'date',year=True, month=True, week=True, shift=False)
    
    #Rename and transform a kind of data.
    statesData=statesData.rename(columns={'fips':'states'})
    statesData.states=statesData.states.astype('int64')

    # Merge the data
    OverallTraqckingCovid=TraqckingCovidDataFrame.merge(statesData,on='state')
    #This code it´s work
    # Get the Clean data though the Json

    #__________Begin Get the Data Analisis________

    #The graph than show the increase from positive case for covid by state in the USA
    #OverallTraqckingCovid['date']=pd.to_datetime(OverallTraqckingCovid.date,format='%Y%m%d')
    IncreasePositive=OverallTraqckingCovid.groupby(["date","name"])["positiveIncrease"].sum().reset_index(inplace=False)
    graphIncreaseCovidbyState=DinamicSeriesTime(IncreasePositive,"positiveIncrease",width=600,height=300)
    resourcesgraphIncreaseCovidbyState=ManageResources.extractResource(graphIncreaseCovidbyState)
    #
    return jsonify({'SeriesTimeGraph':resourcesgraphIncreaseCovidbyState})

@app.route('/ParetoData', methods=['GET'])
def ParetoData():
    
    #This code it´s work
    # Get the Clean data though the Json
    data=requests.get('http://127.0.0.1:5000/GeneratorData')
    if data.status_code==200:
        data=data.json()
    OverallTraqckingCovid=pd.DataFrame(data['DATA'])

    #__________Begin Get the Data Analisis________

    #The Pareto Graph
    casesPositiveByStates=OverallTraqckingCovid.groupby(["name"])["positiveIncrease"].sum().reset_index(inplace=False)
    ParetoCasePositive=ParetoDinamic(casesPositiveByStates,"name","positiveIncrease",width=600,height=400)
    resourcesParetoCasePositive=ManageResources.extractResource(ParetoCasePositive)
    
    return jsonify({'ParetoGraph':resourcesParetoCasePositive})

@app.route('/MapaUSAData', methods=['GET'])
def MapaUSAData():
    
    #This code it´s work
    # Get the Clean data though the Json
    data=requests.get('http://127.0.0.1:5000/GeneratorData')
    if data.status_code==200:
        data=data.json()
    OverallTraqckingCovid=pd.DataFrame(data['DATA'])

    #__________Begin Get the Data Analisis________
        #Map Graph 
    #For this graph I used the data from the Pareto
    #This is important part, becouse this part is for get the cordenates from the states
    name_states=[state['name'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    states_xs=[state['lons'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    states_ys=[state['lats'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    #This is important geographic part, becouse we get a dataFrame wit all the cordenates
    Geographic_data=dict(
        cordenate_x=states_xs,
        cordenate_y=states_ys,
        name=name_states,
    )
    casesPositiveByStates=OverallTraqckingCovid.groupby(["name"])["positiveIncrease"].sum().reset_index(inplace=False)
    GeographicDataFrame=pd.DataFrame(Geographic_data)
    GeographicCasePositiveByStates=casesPositiveByStates.merge(GeographicDataFrame,on="name")
    GraphMapCasePositiveByStates=MapDinamic(GeographicCasePositiveByStates,"positiveIncrease",palette,width=700,height=400)
    resourcesGraphMapCasePositiveByStates=ManageResources.extractResource(GraphMapCasePositiveByStates)

    
    return jsonify({'MaphGraph':resourcesGraphMapCasePositiveByStates})

@app.route('/AlaskaMapGraph')
def AlaskaMapGraph():
    # Get the Clean data though the Json
    data=requests.get('http://127.0.0.1:5000/GeneratorData')
    if data.status_code==200:
        data=data.json()
    OverallTraqckingCovid=pd.DataFrame(data['DATA'])

    casesPositiveByStates=OverallTraqckingCovid.groupby(["name"])["positiveIncrease"].sum().reset_index(inplace=False)
    #This part is only for Alaska
    name_AlaskaAndHawaii=[state['name'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    AlaskaAndHawaii_xs=[state['lons'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    AlaskaAndHawaii_ys=[state['lats'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    #This is important geographic part, becouse we get a dataFrame wit all the cordenates
    AlaskaAndHawaii_data=dict(
        cordenate_x=AlaskaAndHawaii_xs,
        cordenate_y=AlaskaAndHawaii_ys,
        name=name_AlaskaAndHawaii,
    )

    
    AlaskaAndHawaiiDataFrame=pd.DataFrame(AlaskaAndHawaii_data)
    AlaskaAndHawaiiCasePositiveByStates=AlaskaAndHawaiiDataFrame.merge(casesPositiveByStates,on="name")
    rango_limites={
        "lix1":-180,
        "lsx2":-130,
        "liy1":50,
        "lsy2":75}
    AlaskaAndHawaiiCasePositiveByStates=MapDinamic(AlaskaAndHawaiiCasePositiveByStates,"positiveIncrease",palette,width=400,height=400,ranges=rango_limites)
    resourcesAlaskaAndHawaiiCasePositiveByStates=ManageResources.extractResource(AlaskaAndHawaiiCasePositiveByStates)
    return jsonify({'MaphGraphAlaska':resourcesAlaskaAndHawaiiCasePositiveByStates})

@app.route('/GraphTest')
def GraphTest():

    MapaData=requests.get('http://127.0.0.1:5000/MapaUSAData')
    if MapaData.status_code==200:
        MapaData=MapaData.json()
    
    MapaDataAlaska=requests.get('http://127.0.0.1:5000/AlaskaMapGraph')
    if MapaDataAlaska.status_code==200:
        MapaDataAlaska=MapaDataAlaska.json()

    ParetoData=requests.get('http://127.0.0.1:5000/ParetoData')
    if ParetoData.status_code==200:
        ParetoData=ParetoData.json()    

    TimeSeriesData=requests.get('http://127.0.0.1:5000/SeriesTimeData')
    if TimeSeriesData.status_code==200:
        TimeSeriesData=TimeSeriesData.json()    

        

    listResourcesGraphs=[dict(MapaData['MaphGraph']),
                        dict(MapaDataAlaska['MaphGraphAlaska']),
                        dict(ParetoData['ParetoGraph']),
                        dict(TimeSeriesData['SeriesTimeGraph'])]

    #Get the resources from the graphs
    joinResourcesGraphs=ManageResources.joinDictionary(listResourcesGraphs)
    

    return render_template('DASHBOARD/DashBoardTest.html',data=joinResourcesGraphs)
    
"""______________End the back end of the aplication_______________________"""

@app.route('/CovidDashboard')
def CovidDashboard():
    
    
    #__________Begin Get the dataframe master________
    # Define the URL
    traqckingUrl=urlCovid['covidtraqckingHistoric']
    statesUrl=urlCovid['states']

    # Get the data( all the data and row data)
    TraqckingCovidDataFrame=managmenteAPI.conection(traqckingUrl)
    statesData=managmenteAPI.conection(statesUrl)
    
    #Set the date
    TraqckingCovidDataFrame['date']=pd.to_datetime(TraqckingCovidDataFrame.date,format='%Y%m%d')
    TraqckingCovidDataFrame=apply_scalars(TraqckingCovidDataFrame,'date',year=True, month=True, week=True, shift=False)
    
    #Rename and transform a kind of data.
    statesData=statesData.rename(columns={'fips':'states'})
    statesData.states=statesData.states.astype('int64')
    # Merge the data
    OverallTraqckingCovid=TraqckingCovidDataFrame.merge(statesData,on='state')

    #__________End Get the dataframe master________

    #**************Any Idea than I have is put filters in the graph, for make ir more dinamic
    #Answer: **************Yes we have any Idea men**************



    #__________Begin Get the Data Analisis________
    curdoc().theme = 'dark_minimal'

    #The graph than show the increase from positive case for covid by state in the USA
    IncreasePositive=OverallTraqckingCovid.groupby(["date","name"])["positiveIncrease"].sum().reset_index(inplace=False)
    graphIncreaseCovidbyState=DinamicSeriesTime(IncreasePositive,"positiveIncrease",width=600,height=300)
    resourcesgraphIncreaseCovidbyState=ManageResources.extractResourceTheme(graphIncreaseCovidbyState,theme=curdoc().theme)

    #The Pareto Graph
    casesPositiveByStates=OverallTraqckingCovid.groupby(["name"])["positiveIncrease"].sum().reset_index(inplace=False)
    ParetoCasePositive=ParetoDinamicColors(casesPositiveByStates,"name","positiveIncrease",width=600,height=400)
    resourcesParetoCasePositive=ManageResources.extractResourceTheme(ParetoCasePositive,theme=curdoc().theme)

    #Map Graph 
    #For this graph I used the data from the Pareto
    PaletteTurbo=tuple(reversed([Turbo256[i*4] for i in range(63)]))
    #This is important part, becouse this part is for get the cordenates from the states
    name_states=[state['name'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    states_xs=[state['lons'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    states_ys=[state['lats'] for state in states.values() if (state['name']!="Alaska" and state['name']!="Hawaii")]
    #This is important geographic part, becouse we get a dataFrame wit all the cordenates
    Geographic_data=dict(
        cordenate_x=states_xs,
        cordenate_y=states_ys,
        name=name_states,
    )

    GeographicDataFrame=pd.DataFrame(Geographic_data)
    GeographicCasePositiveByStates=casesPositiveByStates.merge(GeographicDataFrame,on="name")
    GraphMapCasePositiveByStates=MapDinamic(GeographicCasePositiveByStates,"positiveIncrease",PaletteTurbo,width=800,height=500)
    resourcesGraphMapCasePositiveByStates=ManageResources.extractResourceTheme(GraphMapCasePositiveByStates,theme=curdoc().theme)

    #This part is only for Alaska
    PaletteTurboAlaska=tuple(reversed([Turbo256[i*4] for i in range(10)]))
    name_AlaskaAndHawaii=[state['name'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    AlaskaAndHawaii_xs=[state['lons'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    AlaskaAndHawaii_ys=[state['lats'] for state in states.values() if (state['name']=="Alaska" or state['name']=="Hawaii")]
    #This is important geographic part, becouse we get a dataFrame wit all the cordenates
    AlaskaAndHawaii_data=dict(
        cordenate_x=AlaskaAndHawaii_xs,
        cordenate_y=AlaskaAndHawaii_ys,
        name=name_AlaskaAndHawaii,
    )

    AlaskaAndHawaiiDataFrame=pd.DataFrame(AlaskaAndHawaii_data)
    AlaskaAndHawaiiCasePositiveByStates=AlaskaAndHawaiiDataFrame.merge(casesPositiveByStates,on="name")
    rango_limites={
        "lix1":-180,
        "lsx2":-130,
        "liy1":50,
        "lsy2":75}
    AlaskaAndHawaiiCasePositiveByStates=MapDinamic(AlaskaAndHawaiiCasePositiveByStates,"positiveIncrease",PaletteTurboAlaska,width=400,height=500,ranges=rango_limites)
    resourcesAlaskaAndHawaiiCasePositiveByStates=ManageResources.extractResourceTheme(AlaskaAndHawaiiCasePositiveByStates,theme=curdoc().theme)

    #Do the list from the resources the graphs
    listResourcesGraphs=[resourcesGraphMapCasePositiveByStates,
                         resourcesAlaskaAndHawaiiCasePositiveByStates,
                         resourcesgraphIncreaseCovidbyState,
                         resourcesParetoCasePositive]
    #Get the resources from the graphs
    joinResourcesGraphs=ManageResources.joinDictionary(listResourcesGraphs)
    

    return render_template('DASHBOARD/CovidDashboard.html',data=joinResourcesGraphs)


if __name__=='__main__':
    app.config.from_object(externalObject['config'])
    app.run()