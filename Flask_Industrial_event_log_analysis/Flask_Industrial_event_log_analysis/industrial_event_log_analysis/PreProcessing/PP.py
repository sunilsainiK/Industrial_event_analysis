from flask_restful import Resource

class preprocess(self):

    def merge(events,value1,value2):
        #Replacing the Nan Value of columns
        events[value1].fillna('No_'+ value1, inplace=True)
        events[value2].fillna('No_'+ value2, inplace=True)
        # merging the columns into new column called event_Type
        events['event_type'] = events[value1]+ "__ " + events[value2].map(str)
        #Dropping the columns which is not required as EDA now based on time and evnt_type
        events = events.drop([value1,value2], axis=1)
        #events.to_csv("C:\\PCK\\events_for_single_robot.csv")
        return events.to_json(orient=records)


    def dataframerename(big_period,small_period,dframe):
        events = dframe.rename(columns={big_period:'big_period',small_period:'small_period'})
        #events.to_csv("C:\PCK\MC_040_R04\MC_040_R04.csv",index=False)
        #checkdataframe(events)
        return events.to_json(orient=records)

    def checkdataframe(events):
        tuple = 'event_type','big_period','small_period'
        if set(['event_type','big_period','small_period']).issubset(events.columns):
           if (len(tuple)==len(events.columns)):
              return {"you can use this dataframe for this algo as it has following columns = {} ".format(tuple)}
           else:
               return{"you cannot use this dataframe for this algo as number of columns is not matching with  required number of  columns which is ={}, {},{}".format(tuple[0],tuple[1],tuple[2])}
        else:
            return {"you cannot use this dataframe for this algo it required following columns={},{},{}".format(tuple[0],tuple[1],tuple[2])}

    def drop(data):
        data  = data.dropna(inplace=True)
        return data.to_json(orient=records)
