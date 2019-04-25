from abc import ABC, abstractmethod
class Run_EDA(ABC):
    def __init__(self,df):
        self.org_df = df
        #self.int_df = org_df
    @abstractmethod
    def getEventProb(df):
        # dropping the bucket because probabilty of event occuring in this data frame is on day basis
        events_no_dup = events.drop(['small_period'], axis=1)
        # drop the duplicate rows
        events_no_dup = events_no_dup.drop_duplicates()
        # creating the pickle for future processing
        #events_no_dup.to_pickle("C:\\PCK\\events_no_dup.pck")
        # calculating the no of days
        days = events_no_dup['big_period'].unique().size
        #print(events_no_dup['big_period'].unique())
        events_count = events_no_dup.groupby(['event_type']).count()
        events_count = events_count.reset_index()
        # calculating the probabilty of the bevent days wise based on probabilty formula
        events_count['prob'] = events_count['big_period'] / days
        # dropping the day column as we goty the probabilty of each daywise event already
        events_count = events_count.drop(['big_period'], axis=1)

        return events_count
    # for calculatin daily and conditional probabilty
    @abstractmethod
    def getEventPostProbs(events, events_probs):
        events_probs_XL = events_probs[events_probs['prob'] > 1.0]
        #if(len(events_probs_XL.index) > 0):
        #print('Too Large Probability')
        events_prob_nan = events_probs[events_probs['prob'].apply(math.isnan)]
        #if (len(events_prob_nan.index) > 0):
        #      print('Prob is nan')


        event_post = getConditionalEventProb(events)
        event_post['post'] = events_probs['prob'] * event_post['c_prob']

        event_post = event_post.drop(['big_period_x','big_period_y', 'c_prob'], axis=1)
        event_post_XL = event_post[event_post['post'] > 1.0]
        #if(len(event_post_XL.index) > 0):
        #     print('Too Large Post')
        event_post_XL = event_post[event_post['post'] > 1.0]
        events_post_nan = event_post[event_post['post'].apply(math.isnan)]
        # if (len(events_post_nan.index) > 0):
        #     print('Prob is nan')
        return event_post

    @abstractmethod
    def getConditionalEventProb(events):
        events['counter'] = 1
        # create a data frame with all information how many events are contained in every bucket (e.g. day or hour)
        # and drop irrelevant columns
        events_in_bucket = events.groupby(['small_period']).count()
        events_in_bucket = events_in_bucket.reset_index()
        events_in_bucket = events_in_bucket.drop(['event_type'], axis=1)
        event_x_in_bucket = events.groupby(['small_period', 'event_type']).count()
        event_x_in_bucket = event_x_in_bucket.reset_index()
        # join the to data frames
        join = pd.merge(event_x_in_bucket, events_in_bucket, on=events.columns[2])
        # calculate the conditional probability of events types in the bucket that specific event is of a specific type
        # or more precisely the share of a specific event type in a bucket
        join['c_prob'] = join['counter_x'] / join['counter_y']
        # drop now irrelevant information bucket
        join = join.drop(events.columns[2], axis=1)
        # cacluate the mean share of an event type in a bucket
        avg_ratio = pd.DataFrame
        avg_ratio = join.groupby(['event_type']).mean()
        # drop irrelvant columns
        avg_ratio = avg_ratio.drop(['counter_x', 'counter_y'], axis=1)
        return avg_ratio.reset_index()

    @abstractmethod
    # filtering the probabilty based on thrasholfd which is define by user
    def filter_events_on_daily_prob(events, daily_prob, threshold):
        join = pd.merge(events, daily_prob, on=['event_type'])
        return_df = join[join['prob'] < threshold]
        return_df.drop(['prob'],axis=1)
        return return_df
    @abstractmethod
    def score_EDA(intial_df,daily_prob,aposteriori):
        events_scoring = pd.merge(intial_df, daily_prob, on=['event_type']
        events_scoring = pd.merge(events_scoring, aposteriori, on=['event_type'], how='outer')
        events_scoring['post'].fillna(1, inplace=True)
        events_scoring['score'] = 1-events_scoring['post']
        score = events_scoring.groupby(['bucket']).mean()
        score['raw_score'] = score['score']
        count = events_scoring.groupby(['bucket']).count()
        score['event_count'] = count['event_type']
        return score

    @abstractmethod
    def genearte_sample(df):
        events_trainings = df.drop(['time'], axis=1)
        return events_trainings

    @abstractmethod
    def result_visualize(df):
        sample_visyalize = dict(type="heatmap",z=ht,x=df.columns, y=df.columns)
        return sample_visyalize



def sample(self,df):
    sample_EDA = Run_EDA.genearte_sample(df)
    return sample_EDA


def train(self,df):
    daily_prob  = Run_EDA.getEventProb(df)
    aposteriori = Run_EDA.getEventPostProbs(df, daily_prob)
    aposteriori = Run_EDA.filter_events_on_daily_prob(aposteriori,daily_prob, daily_threshold=0.5)
    return aposteriori

def score(self,modal_df,intial_df):
    aposteriori = modal_df
    df = intial_df
    daily_prob=Run_EDA.getEventProb(df)
    score=Run_EDA.score_EDA(intial_df,daily_prob,aposteriori)
    v_result = Run_EDA.result_visualize(score)
    return (score,v_result)
