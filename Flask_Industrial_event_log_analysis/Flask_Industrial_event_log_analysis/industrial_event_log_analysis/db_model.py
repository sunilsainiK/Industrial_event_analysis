from app import app, db

#creation of the tables

class user(db.Model):
    user_id = db.Column(db.String(80), primary_key = True)
    prediction = db.Column(JSON)
    project_id = db.Column(db.String(80), unique= False)


    def __init__(self,user_id, prediction, project_id):
        self.user_id = user_id
        self.prediction = prediction
        self.project_id = project_id


class raw_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.user_id') , nullable=False )
    raw_data_set = db.Column(JSON)

    def __init__(self, user_id, raw_data_set):
        self.user_id = user_id
        self.raw_data_set = raw_data_set


class project(db.Model):
    project_id = db.Column(db.String(80), primary_key=True)
    raw_data_id = db.Column(db.Integer, db.ForeignKey('raw_data.id'), nullable=False)
    algo = db.Column(db.String(40))
    user_id = db.Column(db.String(80), db.ForeignKey('user.user_id'))

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





db.create_all()
db.Commit()
