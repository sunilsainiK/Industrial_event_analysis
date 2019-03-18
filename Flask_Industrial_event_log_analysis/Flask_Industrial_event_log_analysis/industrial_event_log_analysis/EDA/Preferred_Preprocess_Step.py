from PreProcessing.PP import *
from  app import  api


api.add_resource(merge,"/api/merge_EDA/<string:column1>/<string:column2>")
api.add_resource(dataframerename,"/api/bucket_EDA/<string:size>")
