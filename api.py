# This is a sample Python script.
import logging
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, HourLocator
# Import Module
import ftplib
from ftplib import FTP
from datetime import datetime


app = Flask(__name__,static_url_path="", static_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/meses', methods=['GET'])
def api_get_mes():
    return jsonify(get_mes())

@app.route('/api/volt', methods=['GET'])
def api_graph_volt():
    return graph_volt()

@app.route('/api/current', methods=['GET'])
def api_graph_current():
    return graph_current()

@app.route('/api/power', methods=['GET'])
def api_graph_power():
    return graph_power()

@app.route('/api/energytot', methods=['GET'])
def api_graph_energytot():
    return graph_energytot()


@app.route('/api/daily', methods=['GET'])
def api_graph_energydaily():
    return graph_energydaily()


def connect_to_db():
    conn = sqlite3.connect('db1')
    return conn

def get_mes():
    meses = []
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM mes")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            mes = {}
            mes["volt"] = i["volt"]
            meses.append(mes)
        print(meses)

    except:
        meses = []

    return meses
def graph_volt_old():
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['volt'] = df['volt'].astype(float)
        df.plot(kind='line', x='date', y='volt', color='red', x_compat=True)
        # use formatters to specify major and minor ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y-%H-%M'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.show()
        # Be sure to close the connection
        plt.savefig('volt.png')
        plt.savefig('templates/volt.png')
        conn.close()

    except Exception as e:
        logging.critical(e, exc_info=True)
    img_dir = 'templates'
    img_list = os.listdir(img_dir)
    img_path = os.path.join(img_dir, 'volt.png')

    return render_template('indexv.html')


def graph_volt():
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['volt'] = df['volt'].astype(float)
        df.plot(kind='line', x='date', y='volt', color='pink', x_compat=True)
        # use formatters to specify major and minor ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y-%H-%M'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.show()
        # Be sure to close the connection
        plt.savefig('power.png')
        plt.savefig('templates/power.png')
        conn.close()

    except Exception as e:
        logging.critical(e, exc_info=True)

    line_labels = df['date']
    line_values = df['volt']
    return render_template('indexv1.html', title='Volt',  max= df['volt'].max(),min=df['volt'].min(),  labels=line_labels, values=line_values)




def graph_current():
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['current'] = df['current'].astype(float)
        df.plot(kind='line', x='date', y='current', color='pink', x_compat=True)
        # use formatters to specify major and minor ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y-%H-%M'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.show()
        # Be sure to close the connection
        plt.savefig('current.png')
        plt.savefig('templates/current.png')
        conn.close()

    except Exception as e:
        logging.critical(e, exc_info=True)
    img_dir = 'templates'
    img_list = os.listdir(img_dir)
    img_path = os.path.join(img_dir, 'current.png')

    return render_template('indexc.html')


def graph_power():
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['powewr'] = df['powewr'].astype(float)
        df.plot(kind='line', x='date', y='powewr', color='pink', x_compat=True)
        # use formatters to specify major and minor ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y-%H-%M'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
        plt.show()
        # Be sure to close the connection
        plt.savefig('power.png')
        plt.savefig('templates/power.png')
        conn.close()

    except Exception as e:
        logging.critical(e, exc_info=True)

    line_labels = df['date']
    line_values = df['powewr']
    return render_template('indexp.html', title='Power', max='100',  labels=line_labels, values=line_values)

def graph_energytot():
    y=[]
    try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['energy'] = df['energy'].astype(float)
        #df.plot(kind='line', x='date', y='energy', color='violet', x_compat=True)
        # use formatters to specify major and minor ticks
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y-%H-%M'))
        #plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        #plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
        #plt.show()
        # Be sure to close the connection
        #plt.savefig('energy.png')
        #plt.savefig('templates/energy.png')
        start = datetime.strptime('21:00:00', '%H:%M:%S').time()
        end = datetime.strptime('21:01:00', '%H:%M:%S').time()
        y = df[df['date'].dt.time.between(start, end)]
        #y = y.dropna()
        print(y)
        #y['energy'] = y['energy'].diff()
        y = y[~y['energy'].isnull()]
        print(y)
        conn.close()

    except Exception as e:
        logging.critical(e, exc_info=True)
    
    line_labels = y['date']
    line_values = y['energy']
    return render_template('indexen.html', title='athroistiki endeiksi', max= y['energy'].max(),min=y['energy'].min(),  labels=line_labels, values=line_values)


def graph_energydaily():
     try:
        # Create a SQL connection to our SQLite database
        conn = connect_to_db()
        # print(meses)
        df = pd.read_sql_query("SELECT * FROM mes", conn)
        ## Set time format and the interval of ticks (every 15 minutes)
        df['date'] = pd.to_datetime(df['date'], format='%c')
        #    df['date']  = datetime.strptime(date_string, "%d %B, %Y")
        df['energy'] = df['energy'].astype(float)
        #df['daily'] = df['energy'].diff(periods=1440)
        #y = df[df.index % 1440 == 1]
        # Filter data between two dates
        print(df['date'])
        start = datetime.strptime('21:00:00', '%H:%M:%S').time()
        end = datetime.strptime('21:01:00', '%H:%M:%S').time()
        y = df[df['date'].dt.time.between(start, end)]
        #y = y.dropna()
        print(y)
        y['daily'] = y['energy'].diff()
        y = y[~y['daily'].isnull()]
        print(y)
        # Be sure to close the connection
        conn.close()
     except Exception as e:
        logging.critical(e, exc_info=True)

     line_labels = y['date']
     line_values = y['daily']
     return render_template('indexdaily.html', title='Daily consum',  max= y['daily'].max(),min=0.9*y['daily'].min(),  labels=line_labels, values=line_values)




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__':
    print_hi('PyCharm')
    # app.debug = True
    # app.run(debug=True)
    app.run()
