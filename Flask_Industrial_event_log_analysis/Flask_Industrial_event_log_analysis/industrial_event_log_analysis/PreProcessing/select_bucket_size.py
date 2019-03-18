from flask_restful import Resource

class Bucket_Size(Resource):
    def get(self,size):
        return {"message":"get is working = {} ".format(size)},200
