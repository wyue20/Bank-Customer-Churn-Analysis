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


app = Flask(__name__)
app.secret_key = '1415926535abcdefg'

def svm_model(test_data):
    print(0)
    df = pd.read_csv('D:\work_space\si681 project\si681 project\clean_bank.csv')
    train_label = df['Exited']
    train_data = df.drop(['Exited'],axis = 1)
    model3 = svm.SVC(kernel='rbf',class_weight={0:1,1:3})#去掉不均衡数据
    model3.fit(train_data, train_label)
    predicted3 = model3.predict(test_data)
    return predict3



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
                print('error')
            else:
                df = pd.DataFrame([score,geography,gender,age,tenure,balance,numofpro,crecard,active,salary],index=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary'])#创建dataframe
                result=svm_model(df)
                print(result)
            if(request.form['numofpro']=='1'):
                return  render_template("main_wy.html")
            else:
                return  render_template("main.html")

    elif request.method == 'GET':
        return  render_template("main_wy.html")

if __name__ == '__main__':
    app.debug = True
    app.run()