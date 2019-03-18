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
import chardet
from pandas.io.json import json_normalize
import requests
from sqlalchemy import text
import psycopg2
from flask_restful import Resource, Api
from app import app
from .Scoring import train_model

api_Eda = Api(app)
api_Eda.add_resource(getEventProb,"/api/train/df_train {}".format())
