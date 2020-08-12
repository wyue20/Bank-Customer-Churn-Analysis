# -*- coding: utf-8 -*-  
from weibo import APIClient 
import requests
import json
import urllib.request #导入urllib.request库
import urllib.parse
from lxml import etree
import io
import sys
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import time
import sqlite3
import os
from flask import Flask, request,render_template,redirect,jsonify,session,make_response,Response
import plotly.graph_objs as go
import plotly
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba  
from datetime import timedelta
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib

app = Flask(__name__)
app.secret_key = '1415926535abcdefg'

def svm_model(test_data):
    path = os.path.join(app.root_path, 'db', 'SVM_model.m')
    model=joblib.load(path)
    print(test_data.T)
    predicted = model.predict(test_data.T)
    return predicted

def rf_model(test_data):
    path = os.path.join(app.root_path, 'db', 'RF_model.m')
    model=joblib.load(path)
    print(test_data.T)
    predicted = model.predict(test_data.T)
    return predicted

def nb_model(test_data):
    path = os.path.join(app.root_path, 'db', 'NB_model.m')
    model=joblib.load(path)
    print(test_data.T)
    predicted = model.predict(test_data.T)
    return predicted

def ann_model(test_data):
    path = os.path.join(app.root_path, 'db', 'ANN_model.m')
    model=joblib.load(path)
    print(test_data.T)
    predicted = model.predict(test_data.T)
    return predicted

def MaxMinNormalization(x,Max,Min):
    x = (x - Min) / (Max - Min)
    return x

@app.route('/',methods=['GET','POST'])
def main_search():
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            numofpro=request.form['numofpro']
            gender=request.form['gender']
            tenure=request.form['tenure']
            geography=request.form['geography']
            crecard=request.form['crecard']
            active=request.form['active']
            score=request.form['score']
            age=request.form['age']
            balance=request.form['balance']
            salary=request.form['salary']
            Model=request.form['Model']
            if not salary or not balance or not age or not score:
                return  render_template("content_result.html",result='error')
            else:
                if gender == "female":
                    gender = 0
                else:
                    gender = 1
                if geography == 'France':
                    geography = 0
                elif geography == 'Spain':
                    geography = 1 
                else:
                    geography = 2

                if active == "yes":
                    active = 1
                else:
                    active = 0

                if crecard == "yes":
                    crecard = 1
                else:
                    crecard = 0
                balance = MaxMinNormalization(float(balance),250898.09,0.0)
                salary = MaxMinNormalization(float(salary),199992.48,11.58)
                df = pd.DataFrame([float(score),geography,gender,float(age),float(tenure),balance,float(numofpro),crecard,active,salary],index=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary'])#创建dataframe
                if(Model=='SVM'):
                    result=svm_model(df)
                    return  render_template("content_result.html",result=result)
                elif(Model=='RF'):
                    result=rf_model(df)
                    return  render_template("content_result.html",result=result)
                elif(Model=='GNB'):
                    result=nb_model(df)
                    return  render_template("content_result.html",result=result)
                elif(Model=='ANN'):
                    result=ann_model(df)
                    return  render_template("content_result.html",result=result)

    elif request.method == 'GET':
        return  render_template("index.html")

if __name__ == '__main__':
    app.run()
