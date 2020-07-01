from flask import Flask, render_template
from flask import request, redirect
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
import os
import sys
import numpy as np
import pandas as pd
import threading
import time
import socket
from flask_socketio import SocketIO, send
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import json
import pandas as pd
from heapq import nlargest

myapp = Flask(__name__)
socketio = SocketIO(myapp)
dictionary = {'PERSON': 'who', 'DATE': 'when', 'ORDINAL': 'which', 'GPE': 'where', 'CARDINAL': 'how many', 'NORP': 'what',
              'ORG': 'where', 'FAC': 'where', 'LOC': 'where', 'PRODUCT': 'what', 'EVENT': 'which', 'WORK_OF_ART': 'what',
              'LAW': 'which', 'LANGUAGE': 'which', 'TIME': 'when', 'PERCENT': 'what percentage', 'MONEY': 'how much', 'QUANTITY': 'how much'}
df = pd.DataFrame(columns = ['Question', 'Answer'])
stopwords = list(STOP_WORDS)
nlp = spacy.load('en')
punctuation = punctuation + '\n'

def resets():
    time.sleep(0.01)
    python = sys.executable
    os.execl(python, python, * sys.argv)

@myapp.route("/", methods=["GET", "POST"])
def index():
    z = threading.Thread(target=resets, args=())
    z.start()
    return render_template('index.html')

@myapp.route("/team", methods=["GET", "POST"])
def team():
    return render_template('team.html')

@myapp.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        return render_template("about.html")
    
    elif request.method == "GET":
        return render_template("index.html")

@myapp.route("/submit", methods=["GET", "POST"])
def upload():
    global df
    if request.method == "POST":
        text = str(request.form['text'])
        to_analyze = text
        jsonfile = question_generation(to_analyze)
        return render_template("QA.html", string1 = jsonfile)

    elif request.method == "GET":
        return render_template("index.html")

def question_generation(to_analyze):
    global df
    summary = str(summarize(to_analyze))[1:-1]
    doc = nlp(summary)
    sent_token = [sent for sent in doc.sents]
    for sent in sent_token:
        new_sent = str(sent)
        doc1 = nlp(new_sent)
        ents = [(x.text, x.label_)
                    for x in doc1.ents]
        for idx, _ in enumerate(ents):
            if new_sent.find(ents[idx][0]) != -1:
                if new_sent.find(ents[idx][0]) == 0:
                    string1 = new_sent.replace(ents[idx][0], dictionary[ents[idx][1]]).replace('.', '?')
                    df = df.append({'Question' : string1.replace(string1[0], string1[0].upper()), 'Answer' : ents[idx][0]}, ignore_index=True)
                else:
                    df = df.append({'Question' : new_sent.replace(' ' + ents[idx][0], ' ' + dictionary[ents[idx][1]]).replace('.', '?'), 'Answer' : ents[idx][0]}, ignore_index=True)
        
    return df.to_json(orient='records')

def summarize(to_analyze):
    doc = nlp(to_analyze)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
    
    max_freq = max(word_freq.values())
    
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    sent_token = [sent for sent in doc.sents]

    sent_score = {}
    for sent in sent_token:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text.lower()]
                else:
                    sent_score[sent] += word_freq[word.text.lower()]
    
    select_len = int(len(sent_token) * 0.5)
    summary = nlargest(select_len, sent_score, key = sent_score.get)
    return summary

    
if __name__ == '__main__':
    # myapp.run(debug=True)
    socketio.run(myapp)