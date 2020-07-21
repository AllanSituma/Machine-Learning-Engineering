#importing libraries
import os
import numpy as np
import flask
import pickle
import json
import pandas as pd
import pickle as p
import psycopg2
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy


#creating instance of the class
app=Flask(__name__)

#psy
connection = psycopg2.connect(user=" ",
                                  password=" ",
                                  host=" ",
                                  port=" ",
                                  database=" ")



clf_path = 'model/random_forest.pkl'
with open(clf_path,'rb') as f:
	model= p.load(f)


#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/predict', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		client_id = request.json
		cursor = connection.cursor()
		query = "select * from public_data_science.feature_table where user_id = {}".format(client_id)
		cursor.execute(query)
		record = cursor.fetchall()
		column_names = [desc[0] for desc in cursor.description]
		df = pd.DataFrame(record,columns = (column_names))
		df_new_one = df.drop(['user_id','min_credit_lender','max_creditline_lender'],axis = 1)
		df_new = df_new_one.fillna(0)
		min_cred = df_new['min_creditline'].values
		max_cred = df_new['max_creditline'].values
		prediction = model.predict(df_new)
		probability = model.predict_proba(df_new)
		cursor.close()
		return jsonify({"max_credit":int(max_cred),
			            "min_credit":int(min_cred),
			            "Repay_score":int(probability[:,0]*1000),
			            "Default_probability":int(probability[:,1]*100),
			            "prediction":int(prediction)
			             
			             })
	else:
		return 'API FINE!'



if __name__ == '__main__':
	app.run(host='82.165.23.225',debug=True)
