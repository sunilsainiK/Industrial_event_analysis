from abstract_algorithm import Algorithm
from pandas import DataFrame
from pandas import Series
import pandas as pd
import numpy as np

class EPA(Algorithm):



    def sample(self,df:DataFrame):#-> DataFrame:
        samples = self.__create_samples(df)
        mapping = self.__create_mapping(df,samples)
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

    def applicable(self, dtypes:Series):
        if 'event_type' not in dtypes.index:
            return False
        if 'big_period' not in dtypes.index:
            return False
        if 'small_period' not in dtypes.index:
            return False
        if len(dtypes) > 3:
            return False
        return True

    ## Note contains a bug!
    def train(self,df:DataFrame):#-> pkl:
        post=  self.__big_probs(df)*self.__small_probs(df)
        model = pd.DataFrame(post).T
        return model

    def __big_probs(self, samples):
        big = samples.groupby('big_period').sum()
        big = big.applymap(lambda x: 0 if x <= 0 else 1)
        sums = big.sum(axis = 0, skipna = True)
        big_p = len(big)
        probs = sums/big_p
        return probs

    ## Note - not yet calculating under the condition that the event appears on that day!
    ## Probably need to iterate!
    def __small_probs(self, samples):
        total = samples.sum(axis=1)
        ratios = samples[samples.columns[1:-2]].div(total, axis=0)
        return ratios.mean()

    def score(self,modal_df:object,intial_df:DataFrame):# -> DataFrame::
        samples = intial_df
        model = modal_df
        prediction = (samples[samples.columns[1:-2]] * model).fillna(1)
        return prediction.applymap(lambda x: 1-x)


    def visualize(self, df:DataFrame):# -> dict:
        return None


    def display_name(self):
        return 'Event Probability Analysis'

    def hint(self, df):
        hints = []
        if 'event_type' not in df.columns:
            hints.append('No "event_type" column. If no suitable column in the data, consider merging columns to create an event type')
        if 'small_period' not in df.columns:
            hints.append('No "small_period" column. Creating a datetime column with changed frequency (e.g. minutes or hours). Select the frequency according to the desired update of the anomaly score (e.g. to update every minutes, set frequency to minutes).')
        if 'big_period' not in df.columns:
            hints.append('No "big_period" column. Creating a datetime column with changed frequency (e.g. minutes or hours). This frequency needs to be bigger then the small_period frequency. Often, the next larger frequency frequency is suitable.')
        if np.dtype('datetime64[ns]') in df.dtypes.tolist():
            hints.append('No timestamp (column with datetime datatype) column in the data. Consider creating such a column, e.g. by applying the "Change to Datetime" Operation or merging several columns like "year", "month", "day" etc into a datetime column.')
        return hints
