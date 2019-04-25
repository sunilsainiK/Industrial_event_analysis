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
#from models import *
import io
import os
import subprocess

from flask_sqlalchemy import SQLAlchemy
from os.path import basename
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
from inspect import formatargspec, getfullargspec
app = Flask(__name__)

app.secret_key =os.urandom(24)



def convert_json_data(dff):
    data = pd.read_json(dff)
    print(data.head())
    return data



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
       cur.execute('SELECT project_name from projects WHERE user_name= %s',(user,))
       project = cur.fetchall()
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
       cur.execute('SELECT user_name FROM users WHERE user_name = %s', (user_name,))
       print('executed')
       user = cur.fetchone()
       print('fetched')
       if not user:
           print(user_name)
           cur.execute('INSERT INTO users (user_name) VALUES(%s)', (user_name,))
           connection.commit()
           print('user inserted')
           project = 'no project'
           cur.close()
           connection.close()
           return project
       if user:
           print('in user',user_name)
           cur.execute('SELECT project_name from projects WHERE user_name= %s',(user_name,))
           project = cur.fetchall()
           print('project fetched')
       if not project:
           print('no project')
           project = 'no project'
           cur.close()
           connection.close()
           return project
       if  project:
           project_table=[]
           i=1
           for i in range(len(project)):
                cur.execute('SELECT raw_data_name , project_name FROM raw_data WHERE  project_name=%s', (project[i]))
                pr_user=cur.fetchall()
                project_table.append(pr_user)
           cur.close()
           connection.close()
           print('got project')
           return jsonify(project_table)
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

#get attribute
@app.route('/get_pre_Args', methods=["GET"])
def algo_args():
    alg_args = request.args.get('algs')
    alg = alg_args
    alg_args = alg_args+'.py'
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
                                    if entry.name == alg_args:
                                        pkl=os.path.join(file_path,alg_args)
                                        mdl = importlib.machinery.SourceFileLoader(alg,pkl).load_module()
                                        attr_Name=getattr(mdl,'run')
                                        prep_result = formatargspec(*getfullargspec(attr_Name))
                                        prep_result = prep_result.replace('*col_name','')
                                        prep_result = prep_result.replace('**kwargs','')
                                        print(prep_result)
                                        l_option=re.sub('[^A-Za-z0-9]+', ',', prep_result)
                                        print(l_option)
                                        l_option = l_option.split(',')
                                        oplen=''
                                        if 'options' in l_option:
                                            for i in reversed(range(len(l_option))):
                                                if not(l_option[i]=='options'):
                                                   oplen+=','+(l_option[i])
                                                else:
                                                    break
                                        return oplen

#get attribute
@app.route('/run_preprocess', methods=["GET"])
def run_algs():
    pre_pro_data = request.get_json(force=True)
    data_for_process = convert_json_data(pre_pro_data)
    prep_run = request.args.getlist('prestep_run')
    opt = request.args.get('opt')
    print(opt)
    alg = request.args.get('optedprepro')
    print(alg)
    opti_text = request.args.get('optional_text')
    alg_args = alg+'.py'
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
                                    if entry.name == alg_args:
                                        pkl=os.path.join(file_path,alg_args)
                                        print(pkl)
                                        mdl = importlib.machinery.SourceFileLoader(alg,pkl).load_module()
                                        args_list={'opt':opt,'df':alg,'col':prep_run,'opti_text':opti_text}
                                        print('run')
                                        attr_Name=getattr(mdl,'run')(data_for_process,prep_run,args_list)
                                        #prep_result = setattr(mdl,alg,(prep_run, opt, alg))
                                        prep_result = attr_Name
                                        prep_result.to_csv('inter_result')
                                        print(prep_result.head())
                                        return prep_result.to_json()

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
#@app.route('/run_preprocess', methods=["GET"])
#def run_pre():
#    prep_run = request.args.get('prestep_run')
#    print(prep_run)
#    dir = os.path.dirname(os.path.realpath(__file__))
#    for root, dirs, files in os.walk(dir, topdown=False):
#        for name in dirs:
#            if name == 'PreProcessing':
#                file_path = os.path.join(root, name)
#                with os.scandir(file_path) as entries:
#                    for entry in entries:
#                        if entry.is_file():
#                            if not entry.name.startswith('_'):
#                                if entry.name.endswith('.py'):
#                                    if entry.name[0]== prep_run:
#                                        prep_result = subprocess.call(entry)
#                    return(prep_result)

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
    project = request.args.get('pr')
    file_name = request.args.get('filename')

    connection = pg2.connect(user='postgres',password='sunil', host='127.0.0.1', port='5432',
    database='Event_Analysis')
    cur = connection.cursor()
    cur.execute('INSERT INTO raw_data (project_name, raw_data_name , raw_data_sample) VALUES(%s,%s,%s)',(project, file_name, data))
    connection.commit()
    print('commited')
    cur.execute('SELECT raw_data_sample FROM raw_data WHERE raw_data_name =%s',(file_name,))
    #'SELECT raw_data_sample  FROM  raw_data INNER JOIN  projects ON raw_data.project_name = projects.project_name')
    raw_data_project = cur.fetchall()
    print('raw data fetched')
    cur.close()
    connection.close()
    print('about to enter')
    with open('data_json', 'w') as f:
         json.dump(raw_data_project, f)
    jdf = open('data_json')
    df_json = json.load(jdf)
    print(df_json)
    df = pd.DataFrame(df_json)
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

@app.route('/run_preprocess_class', methods=["GET"])
def run_algs_class():
    prep_run = request.args.getlist('prestep_run')
    opt = request.args.get('opt')
    print(opt)
    alg = request.args.get('optedprepro')
    print(alg)
    opti_text = request.args.get('optional_text')
    alg_args = alg+'.py'
    df_1 = pd.read_csv('df_raw')
    pmc = alg.run(df_1,{'opt':opt,'df':alg,'col':prep_run,'opti_text':opti_text})
    attr_Name=getattr(pmc,alg)()
    print(attr_Name)
    return 'hi'





if __name__ == '__main__':
    app.run()
