#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1. import Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlite3 as sl3



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    return (
        "/api/v1.0/precipitation : Return a JSON list of precipitation and data <br/>"
        "/api/v1.0/stations : Return a JSON list of stations from the dataset<br/>"
        "/api/v1.0/tobs : Return a JSON list of Temperature Observations (tobs) for the previous year<br/>"
        "/api/v1.0/YYYY-MM-DD and /api/v1.0/YYYY-MM-DD/YYYY-MM-DD : Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"
        )
        

@app.route("/api/v1.0/precipitation")
def precipitation():
    database_path ="Resources/hawaii.sqlite"
    conn = sl3.connect(database_path)
    df_main = pd.read_sql_query("SELECT date as Date,prcp as Precipitation FROM measurement",conn).dropna().sort_values(by="Date").reset_index(drop = True)
    dict_prcp = df_main.to_dict("records")
    return jsonify(dict_prcp)

@app.route("/api/v1.0/stations")
def station():
    database_path ="Resources/hawaii.sqlite"
    conn = sl3.connect(database_path)
    df_main = pd.read_sql_query("SELECT station FROM station",conn).reset_index(drop = True)
    dict_station = tuple(df_main.to_dict("records"))
    return jsonify(dict_station)

@app.route("/api/v1.0/tobs")
def Temperature():
    database_path ="Resources/hawaii.sqlite"
    conn = sl3.connect(database_path)
    df_main = pd.read_sql_query("SELECT tobs as Temperature FROM measurement WHERE (date > '2015-12-31') AND (date < '2017-01-01')",conn).reset_index(drop = True)
    dict_temp = tuple(df_main.to_dict("records"))
    return jsonify(dict_temp)

@app.route("/api/v1.0/<start_date>")
def Temp_by_period(start_date):
    database_path ="Resources/hawaii.sqlite"
    conn = sl3.connect(database_path)
    df_main = pd.read_sql_query(f"SELECT tobs as Temperature FROM measurement WHERE date > '{start_date}'",conn).dropna().reset_index(drop = True)
    temp_min = min(df_main["Temperature"])
    temp_max = max(df_main["Temperature"])
    temp_mean = round(np.mean(df_main["Temperature"]),2)
    temp_dict = {"Minimum Temperature": temp_min , 'Maximum Temperature': temp_max, "Average Temperature": temp_mean} 
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Temp_by_period2(start_date,end_date):
    database_path ="Resources/hawaii.sqlite"
    conn = sl3.connect(database_path)
    df_main = pd.read_sql_query(f"SELECT tobs as Temperature FROM measurement WHERE date > '{start_date}' AND date < '{end_date}'",conn).dropna().reset_index(drop = True)
    temp_min = min(df_main["Temperature"])
    temp_max = max(df_main["Temperature"])
    temp_mean = round(np.mean(df_main["Temperature"]),2)
    temp_dict = {"Minimum Temperature": temp_min , 'Maximum Temperature': temp_max, "Average Temperature": temp_mean} 
    temp_dict 
    return jsonify(temp_dict)



if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:



