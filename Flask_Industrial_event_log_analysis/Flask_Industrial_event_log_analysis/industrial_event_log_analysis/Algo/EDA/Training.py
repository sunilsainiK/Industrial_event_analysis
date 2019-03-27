from flask_restful import Resource

def getEventProb(events):
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

# filtering the probabilty based on thrasholfd which is define by user
def filter_events_on_daily_prob(events, daily_prob, threshold):
   join = pd.merge(events, daily_prob, on=['event_type'])
   return_df = join[join['prob'] < threshold]
   return_df.drop(['prob'],axis=1)
   return return_df

def getScoreLockUp(score):
   scores = score[score['score'] > 0.0].copy()
   max = scores['score'].max()
   min = scores['score'].min()
  # print('Scores max ' + str(max))
  # print('Scores min ' + str(min))
   scores['cat'] = pd.cut(scores['score'], 500)
   density_scores = scores.groupby('cat').count()
   count = len(scores.index)
   density_scores['prob'] = density_scores['score'] / count
   density_scores.sort_index(inplace=True, ascending=False)
   density_scores['cumsum'] = density_scores['prob'].cumsum()
   #density_scores = density_scores.drop(['production_line', 'cell', 'production_line',  'prob_x', 'prob_y', 'timestamp'], axis=1)
   density_scores['cat'] = density_scores.index.astype(str)
   density_scores['low'] = density_scores['cat'].apply(getLower)
   density_scores['up'] = density_scores['cat'].apply(getUpper)
   #density_scores = density_scores.drop(['post', 'score', 'prob', 'cat', 'robot'], axis=1)
   density_scores[['low', 'up']] = density_scores[['low', 'up']].apply(pd.to_numeric)
   return density_scores

# Generalize the Meta data function if the filetr is applied or not  for UI purpose only
def addMetadata(query,scores, engine,values_dataframes,column_to_add,value_to_merge):
   scores[column_to_add]=value_to_merge
   dfmetadata = values_dataframes
   return pd.merge(dfmetadata, scores, on=column_to_add)

def lookup(x):

   df = lookup_table[(lookup_table['low']<x)&(lookup_table['up'] >= x)]
   max = lookup_table['up'].max()
   min = lookup_table['low'].min()
   if(len(df.index) == 0):
       if(max <= x):
           return 1
       if(min >= x):
           return 0
   else:
       y = df['cumsum'][0]
   if(math.isnan(x)):
       return float('nan')
   return y

def getLower(x):
   sci = re.compile('(\d*.\d*e-\d\d)')
   norm = re.compile('([0,1]\.\d*)')
   s = x.split(',')[0]
   y = sci.search(s)
   if(y):
       return y.group(1)
   y =norm.search(s)
   if(y):
       return y.group(1)
   else:
       sys.exit('Could not match lower bound of '+s)

def getUpper(x):
   sci = re.compile('(\d*.\d*e-\d\d)')
   norm = re.compile('([0,1]\.\d*)')
   s = x.split(',')[1]
   y = sci.search(s)
   if(y):
       return y.group(1)
   y =norm.search(s)
   if(y):
       return y.group(1)
   else:
       sys.exit('Could not match upper bound of '+s)


def train(self,df):
    daily_prob = getEventProb(df)
    aposteriori = getEventPostProbs(df, daily_prob)
    aposteriori = filter_events_on_daily_prob(aposteriori,daily_prob, daily_threshold=0.5)
    return aposteriori
