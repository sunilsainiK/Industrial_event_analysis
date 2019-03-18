from flask import Flask,render_template,url_for,request, jsonify
from flask_restful import Resource, Api
from app import app




api = Api(app)
#api.add_resource(preprocess,"/api/merge/<string:column1>/<string:column2>")
#api.add_resource(Bucket_Size,"/api/bucket/<string:size>")
