from flask_restful import Resource
from .EDA_train_Score import train_model_EDA

class train_EDA(train_model_EDA):
    def train(self,events_trainings):
        events_trainings.to_pickle("events_trainings.pck")
        daily_prob = train_model_EDA.getEventProb(events_trainings)
        daily_prob.to_pickle("daily_prob.pck")
        aposteriori = train_model_EDA.getEventPostProbs(events_trainings, daily_prob)
        aposteriori = train_model_EDA.filter_events_on_daily_prob(aposteriori,daily_prob, daily_threshold)
        aposteriori.to_pickle("aposteriori.pck")
        return aposteriori
