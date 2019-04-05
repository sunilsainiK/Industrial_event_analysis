from flask import Flask,render_template,url_for,request, jsonify, send_from_directory, session
from flask_restful import Resource, Api
import pandas as pd
import sys
from datetime import datetime
from sqlalchemy import create_engine
import os
import getpass
import re
import math
import numpy as np
import json
import urllib
import chardet
import importlib
from pandas.io.json import json_normalize
import requests
import psycopg2 as pg2
from sqlalchemy.orm import sessionmaker
from models import *
import io
import os
import subprocess
from  PreProcessing import *
from flask_sqlalchemy import SQLAlchemy
from os.path import basename
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text

app = Flask(__name__)



app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:sunil@localhost:5432/Event_Analysis"

db = SQLAlchemy(app)
conn = pg2.connect(database='Event_Analysis', user='postgres', password='sunil')
cur = conn.cursor()


app.secret_key =os.urandom(24)


def insert_raw_data(data, user):
    newUser = user
    rawdata = data
    new_data = raw_data(newUser, rawdata)
    db.session.add(new_data)
    db.session.commit()



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
       project = request.args.get('project')
       user = request.args.get('user')
       new_project = project(user,project)
       db.session.add(new_project)
       db.session.commit()
    if request.method == 'GET':
       project_name = request.args.get('pr')
       print(project_name)
       cur.execute('SELECT * FROM project')
       project = cur.fetchall()
       if project=='':
           project =='table is empty'
       #project = project.query.filter_by(user_id=project_name).all()
       return project


#Algo Details
@app.route('/Algo_info', methods=["GET"])
def Algo_description_page():
    folder = request.args.get('folder')
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if folder == name:
                file_path = os.path.join(root, name)
                for r, d, f in os.walk(file_path, topdown=False):
                    for file in f:
                        if file.endswith(".html"):
                            Algo_content_info = file
                            return send_from_directory(file_path, Algo_content_info)


#Preprossing Information
@app.route('/preprocess_Info', methods=["GET"])
def pre_info():
    prep_info = request.args.get('prestep_info')
    prep_info=prep_info+'.html'
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if name == 'PreProcessing':
                file_path = os.path.join(root, name)
                for r, d, f in os.walk(file_path, topdown=False):
                    for file in f:
                        if file.endswith(".html"):
                            if file==prep_info:
                                Prep_content_info = file
                                return send_from_directory(file_path, Prep_content_info)


@app.route('/run_preprocess', methods=["GET"])
def run_pre():
    prep_run = request.args.get('prestep_run')
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if name == 'PreProcessing':
                file_path = os.path.join(root, name)
                with os.scandir(file_path) as entries:
                    for entry in entries:
                        if entry.is_file():
                            if not entry.name.startswith('_'):
                                if entry.name.endswith('.py'):
                                    if entry.name[0]== prep_run:
                                        prep_result = subprocess.call(entry)
                                        return(prep_result)

#preprocessing
@app.route('/preprocess', methods=["GET"])
def prepropackage():
    info = request.args.get('prepackage')
    prepropacklist = ''
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if info == name:
                file_path = os.path.join(root, name)
                with os.scandir(file_path) as entries:
                    for entry in entries:
                        if entry.is_file():
                            if not entry.name.startswith('_'):
                                if entry.name.endswith('.py'):
                                    prepropacklist+=','+os.path.splitext(entry.name)[0]
                    return prepropacklist



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
