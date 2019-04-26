from Abstract_Algorithm import Algorithm
from pandas import DataFrame
import pandas as pd

class EDA(Algorithm):
    def sample(self,df:DataFrame):#-> DataFrame:
        samples = self.__create_samples(df)
        mapping = self.__create_mapping
        return {'samples':samples,'mapping':mapping}

    def __create_samples(self, df:DataFrame):
        periods = df[['small_period','big_period']].drop_duplicates()
        events_count = df.groupby(['small_period','event_type']).count().reset_index()
        events_count = events_count.pivot(index='small_period', columns='event_type', values='big_period').reset_index().fillna(0)
        events_count = events_count.merge(periods,on='small_period',how='left')
        return events_count

    def __create_mapping(self, df, samples):
        mapping = {}
        for row in samples.itertuples():
            key = row[0]
            small_period = row[1]
            value = df[df['small_period'] == small_period].index.to_list()
            mapping[key] = value
        return mapping


    def train(self,df:DataFrame):#-> pkl:
        post=  self.big_probs(samples)*self.small_probs(samples)
        model = pd.DataFrame(post).T
        return model

    def big_probs(self, samples):
        big = samples.groupby('big_period').sum()
        big = daily.applymap(lambda x: 0 if x <= 0 else 1)
        sums = daily.sum(axis = 0, skipna = True)
        big_p = len(big)
        probs = sums/big_p
        return probs

    ## Note - not yet calculating under the condition that the event appears on that day!
    ## Probably need to iterate!
    def small_probs(self, samples):
        total = samples.sum(axis=1)
        ratios = samples[samples.columns[1:-2]].div(total, axis=0)
        return ratios.mean()

    def score(self,modal_df:object,intial_df:DataFrame):# -> DataFrame::
        prediction = (samples[samples.columns[1:-2]] * model).fillna(1)
        return prediction.applymap(lambda x: 1-x)


    def visualize(self, df:DataFrame):# -> dict:
        return None
