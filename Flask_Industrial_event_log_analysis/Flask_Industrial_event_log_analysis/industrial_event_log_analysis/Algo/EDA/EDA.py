
class EDA(Algorithm):
    
    
    def sample(self,df:DataFrame):#-> DataFrame:
        samples = self.create_samples(df)
        mapping = create_mapping
        return {'samples':samples,'mapping':mapping}
        
    def create_samples(self, df:DataFrame):
        periods = events[['small_period','big_period']].drop_duplicates()
        events_count = events.groupby(['small_period','event_type']).count().reset_index()
        events_count = events_count.pivot(index='small_period', columns='event_type', values='big_period').reset_index().fillna(0)
        events_count = events_count.merge(periods,on='small_period',how='left')
        return events_count
    
    def create_mapping(self, df, samples):
        mapping = {}
        for row in samples.itertuples():
            key = row[0]
            small_period = row[1]
            value = df[df['small_period'] == small_period].index.to_list()
            mapping[key] = value
        return mapping
            
   
    def train(self,df:DataFrame):#-> pkl:
        return None

    def score(self,modal_df:object,intial_df:DataFrame):# -> DataFrame::
        return None

   
    def visualize(self, df:DataFrame):# -> dict:
        return None