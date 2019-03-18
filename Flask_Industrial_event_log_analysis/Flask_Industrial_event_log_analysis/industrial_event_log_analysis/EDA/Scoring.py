from flask_restful import Resource
from .EDA_train_Score import train_model_EDA
from .Training import train_EDA
import pandas as pd


class score_EDA(train_model_EDA,train_EDA):
    def score(self,events_trainings,robot,value1,query,engine,postGressDataFrame):
        events_scoring = pd.read_pickle("events_trainings.pck")
        daily_prob = pd.read_pickle("daily_prob.pck")
        aposteriori = pd.read_pickle("aposteriori.pck")
        events_scoring = events_scoring.drop(['counter'], axis=1)
        events_scoring = pd.merge(events_scoring, daily_prob,on=['event_type'])
        events_scoring = pd.merge(events_scoring, aposteriori, on=['event_type'], how='outer')
        events_scoring['post'].fillna(1, inplace=True)
        events_scoring['score'] = 1-events_scoring['post']
        score = events_scoring.groupby(['small_period']).mean()
        score['raw_score'] = score['score']
        count = events_scoring.groupby(['small_period']).count()
        score['event_count'] = count['event_type']
        score=addMetadata(query,score, engine,postGressDataFrame,column_to_add=robot,value_to_merge=value1)
        if 'event_type' in score.columns:
            score = score.drop(['prob_x','prob_y','event_type'], axis=1)
        else:
            score = score.drop(['prob_x','prob_y'], axis=1)
        lookup_table = train_model_EDA.getScoreLockUp(score)
        score['cum_score'] = score['score'].apply(lookup)
        score['norm_score'] = score['cum_score']*100
        score = score.drop(['cum_score','raw_score'], axis=1)
        return score.to_json(orient=records)
