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
from importlib import import_module
from pandas.io.json import json_normalize
import requests
import psycopg2 as pg2
from sqlalchemy.orm import sessionmaker
from models import *
import io
import os
import subprocess
import  PreProcessing
from flask_sqlalchemy import SQLAlchemy
from os.path import basename
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
from inspect import formatargspec, getfullargspec
app = Flask(__name__)



#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:sunil@localhost:5432/Event_Analysis"

db = SQLAlchemy(app)

app.secret_key =os.urandom(24)

@app.route('/check_project', methods=['GET','POST'])
def check_project():
    if request.method =='POST':
       project = request.args.get('project')
       print(project)
       user = request.args.get('user')
       print(user)
       connection = pg2.connect(user='postgres',password='sunil', host='127.0.0.1', port='5432',
       database='Event_Analysis')
       cur = connection.cursor()
       cur.execute('INSERT INTO projects (user_name, project_name)  VALUES(%s,%s)',(user,project))
       connection.commit()
       print('commited')
       cur.close()
       connection.close()
       return 'data is saved'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
       user_name = request.args.get('pr')
       print(user_name)
       connection = pg2.connect(user='postgres',password='sunil', host='127.0.0.1', port='5432',
       database='Event_Analysis')
       print('connected')
       cur = connection.cursor()
       cur.execute('SELECT project_name FROM projects WHERE user_name=%s;', (user_name,))
       print('executed')
       project = cur.fetchall()
       print('feteched')
       print(project)
       if not project:
           cur.execute('SELECT user_name FROM users WHERE user_name = %s', (user_name,))
           user = cur.fetchone()
           if not user:
               print(user_name)
               cur.execute('INSERT INTO users (user_name) VALUES(%s)', (user_name,))
               connection.commit()
               print('user inserted')

       cur.close()
       connection.close()
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

@app.route('/get_pre_Args', methods=["GET"])
def algo_args():
    alg_args = request.args.get('algs')
    alg = alg_args
    print(alg)
    alg_args = alg_args+'.py'
    print(alg_args)
    dir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if name == 'PreProcessing':
                print(name)
                file_path = os.path.join(root, name)
                with os.scandir(file_path) as entries:
                    for entry in entries:
                        if entry.is_file():
                            if not entry.name.startswith('_'):
                                if entry.name.endswith('.py'):
                                    print(entry.name)
                                    if entry.name== alg_args:
                                        print(alg_args)
                                        pkl=os.path.join(file_path,alg_args)
                                        print(pkl)
                                        mdl = importlib.machinery.SourceFileLoader(alg,pkl).load_module()
                                        print(mdl)
                                        attr_Name=getattr(mdl,alg)
                                        prep_result = formatargspec(*getfullargspec(attr_Name))
                                        return prep_result

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

#runpackage
@app.route('/run_preprocess', methods=["GET"])
def run_pre():
    prep_run = request.args.get('prestep_run')
    print(prep_run)
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
                                        print(prep_run)
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
    user = request.args.get('use')
    file_name = request.args.get('filename')
    with open('data_json', 'w') as f:
         json.dump(data, f)
    jdf = open('data_json')
    df_json = json.load(jdf)
    df = pd.DataFrame(eval(df_json ))
    connection = pg2.connect(user='postgres',password='sunil', host='127.0.0.1', port='5432',
    database='Event_Analysis')
    cur = connection.cursor()
    cur.execute('INSERT INTO raw_data (user_name, r_data, raw_data) VALUES(%s,%s,%s)', (user, data, file_name))
    connection.commit()
    print('commited')
    cur.execute('SELECT r_data  FROM  raw_data INNER JOIN  projects ON raw_data.user_name = projects.user_name')
    raw_data_user = cur.fetchall()
    cur.close()
    connection.close()
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
