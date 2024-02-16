from flask import Flask, request, render_template, redirect
from emotiv import App
from cortex import Cortex
import pandas as pd
from dotenv import load_dotenv
import os
import random
from threading import Thread
from collections import defaultdict
load_dotenv()

EMOTIV_CLIENT_ID = str(os.getenv("EMOTIV_CLIENT_ID"))
EMOTIV_CLIENT_SECRET = str(os.getenv("EMOTIV_CLIENT_SECRET"))

app = Flask(__name__,
            static_url_path='', 
            static_folder='.', template_folder="./templates")

current_device = None
worker_thread = None
subject_id = 0
question_counters = defaultdict(lambda: -1)

def save_results(path):
    df = pd.read_csv("/Users/mkojro/Documents/bachelors-thesis/emotiv-connection/results/Record title_EPOCX_211020_2024.02.14T13.56.26+01.00.md.pm.bp.csv", skiprows=1)
    records = df.to_dict('records')
    # this can be inserted into mongo
    pass

@app.post('/recordings')
def create_recording():
    # 1. start recording
    # 2. return recording id
    global current_device
    current_device = App(Cortex(
        client_id=EMOTIV_CLIENT_ID,
        client_secret=EMOTIV_CLIENT_SECRET,
        debug_mode=True,
    ))
    current_device.start()

@app.get('/recordings')
def get_recordings():
    # Export recording to some nice format
    pass

@app.post('/recordings/<recording_id>/stop')
def stop(recording_id):
    global current_device
    App.stop_recording(current_device)
    save_results()

@app.post('/markers')
def create_marker():
    # 1. Check if the recording id matches current recording
    # 2. If true inject marker
    body = dict(request.json)
    App.injcect_marker(current_device, body.get('value'), body.get('label'))

@app.post('/answers/<id>')
def create_answer(id):
    # Create answert for a given recording and question
    print(request.form)
    global question_counters
    global current_device
    questions = ["2+2=4", "3+3=12"]

    if current_device is None:
        return render_template('error.html', error_title="Nie mozna nawiązac polaczenia z zestawem EEG", error_text="Zestaw nie jest połączony"), 286

    if current_device.error is not None:
        return render_template('error.html', error_title="Błąd zestawu EEG", error_text=current_device.error), 286

    current_question = questions[question_counters[id]]
    question_counters[id] += 1
    if question_counters[id] >= len(questions):
        App.stop_recording(current_device.c)
        return render_template('bye.html'), 286

    next_question = questions[question_counters[id]]
    App.injcect_marker(current_device.c, id, next_question)
    return render_template("stimuli_form.html", question=next_question) 

@app.get('/devices')
def get_devices():
    # list devices connected to the computer
    pass

@app.get('/end')
def end():
    global current_device
    App.stop_recording(current_device.c)
    return redirect('.')

@app.get('/')
def home():
    return render_template("user.html")

@app.get('/app')
def stimuli():
    print(request.form)
    print(request.args.to_dict())
    global current_device
    global worker_thread
    global subject_id
    del worker_thread
    subject_id += 1
    current_device = App(Cortex(
        client_id=EMOTIV_CLIENT_ID,
        client_secret=EMOTIV_CLIENT_SECRET,
        debug_mode=False,
        url=request.args.get("emotiv_adress")
    ), lambda x: None)
    worker_thread = Thread(target=current_device.start)
    worker_thread.start()
    return render_template("stimuli.html", id=subject_id)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9090)