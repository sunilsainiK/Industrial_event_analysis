from flask import Flask,render_template,url_for,request, jsonify, send_from_directory
from flask_restful import Resource, Api
import pandas as pd
import sys
from datetime import datetime
from sqlalchemy import create_engine
import os
from flask_sqlalchemy import SQLAlchemy
import getpass
import re
import math
import numpy as np
import json
import urllib
import chardet
from pandas.io.json import json_normalize
import requests
from sqlalchemy import text
import psycopg2
import io
import os
#from Algo import EDA, EDA_Naive_Bayes

from os.path import basename
app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:sunil@localhost:5432/Industrial_Event_log_Analysis"

db = SQLAlchemy(app)



def insert_raw_data(data, user):
    newUser = user
    rawdata = data
    new_data = raw_data(newUser, rawdata)
    db.session.add(new_data)
    db.session.commit()


@app.route('/Algo_info', methods=["GET"])
def Algo_description_page():
    folder = request.args.get('folder')
    print(folder)
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if folder == name:
                file_path = os.path.join(root, name)
                print(file_path)
                for r, d, f in os.walk(file_path, topdown=False):
                    for file in f:
                        if file.endswith(".html"):
                            Algo_content_info = file
                            return send_from_directory(file_path, Algo_content_info)









@app.route('/data_summary', methods=["POST"])
def data_summary():
    data = request.get_json(force=True)
    with open('data_json', 'w') as f:
         json.dump(data, f)
    jdf = open('data_json')
    df_json = json.load(jdf)
    df = pd.DataFrame(eval(df_json ))
    df.to_csv('df_raw',index=False)
    df_1 = pd.read_csv('df_raw')
    sum_df_1 = raw_data_summary(df_1)
    return sum_df_1.to_json()

def raw_data_summary(dd_raw):
    raw_summary = dd_raw.count()
    return raw_summary

@app.route('/files_name', methods=["GET"])
def dirname():
    dir = os.path.dirname(os.path.realpath(__file__))
    directory_list = list()
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))
    return jsonify(directory_list)
if __name__ == '__main__':

    app.run()
