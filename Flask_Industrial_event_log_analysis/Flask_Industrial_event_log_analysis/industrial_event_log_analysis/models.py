from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
from app import db
import psycopg2


class user(db.Model):
    user_id = db.Column(db.String(80), primary_key = True)
    project_id = db.Column(db.String(80), primary_key = True)
    prediction = db.Column(JSON)




    def __init__(self,user_id, prediction, project_id):
        self.user_id = user_id
        self.prediction = prediction
        self.project_id = project_id


class raw_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80))
    raw_data_set = db.Column(JSON)

    def __init__(self, user_id, raw_data_set):
        self.user_id = user_id
        self.raw_data_set = raw_data_set


class project(db.Model):
    project_id = db.Column(db.String(80), primary_key=True)
    raw_data_id = db.Column(db.Integer)
    algo = db.Column(db.String(40))
    user_id = db.Column(db.String(80))

    def __init__(self, project_id, raw_data_id, algo, user_id):
        self.project_id = project_id
        self.raw_data_id =raw_data_id
        self.algo = algo
        self.user_id = user_id


class reviwer(db.Model):
    project_id = db.Column(db.String(80), primary_key = True)
    user_id = db.relationship('project_id', backref='user', lazy='dyanmic')

    def __init__(self, project_id, user_id ):
        self.project_id = project_id
        self.user_id = user_id

class sample_data(db.Model):
    sample_ID = db.Column(db.Integer, primary_key = True)
    sample_Data  = db.Column(JSON)
    trained_model = db.Column(BYTEA)
    def __init__(self, sample_ID, sample_Data, trained_model):
        self.sample_ID = sample_ID
        self.sample_Data =  sample_Data
        self.preprared_data = preprared_data
        self.trained_model = trained_model



class prepared_data(db.Model):
    prepared_id = db.Column(db.String(80), primary_key = True)
    project_ID = db.Column(db.Integer)
    preprared_data = db.Column(JSON)
    sample_ID = db.Column(db.Integer)
    def __init__(self, prepared_id, project_ID, prepared_data, sample_ID):
        self.prepared_id = prepared_id
        self.project_ID =  project_ID
        self.preprared_data = preprared_data
        self.sample_ID = sample_ID

class prediction(db.Model):
    prediction_id = db.Column(db.Integer, primary_key = True)
    sample_id = db.relationship('prepared_id', backref='prpared_data')
    analysis_model_name = db.Column(db.String(40))
    score = db.Column(db.Float)
    model_id = db.Column(db.Integer)
    def __init__(self, sample_id, analysis_model_name, score, model_id):
        self.sample_id = sample_id
        self.analysis_model_name =  analysis_model_name
        self.score = score
        self.model_id = model_id

class trained_model_result(db.Model):
    model_id = db.Column(db.Integer, primary_key = True)
    model = db.Column(BYTEA)
    project_id = db.Column(db.Integer)
    parameter = db.Column(JSON)
    def __init__(self, model_id, model, project_id, parameter):
        self.model_id = model_id
        self.model = model
        self.project_id = project_id
        self.parameter = parameter



class feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key = True)
    user_ID = db.Column(db.String(80))
    prediction = db.Column(db.Integer)
    rating = db.Column(JSON)
    feedback = db.Column(JSON)
    def __init__(self, user_ID, prediction, rating, feedback):
        self.user_ID = user_ID
        self.prediction = prediction
        self.rating = rating
        self.feedback = feedback


















#db.create_all()
#db.Commit()
