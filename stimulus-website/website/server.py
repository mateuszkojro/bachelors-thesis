from flask import Flask, request, render_template, redirect
from emotiv import App
from cortex import Cortex
import pandas as pd
from dotenv import load_dotenv
import os
import random
from uuid import uuid4
from threading import Thread
from collections import defaultdict
import json
load_dotenv()

EMOTIV_CLIENT_ID = str(os.getenv("EMOTIV_CLIENT_ID"))
EMOTIV_CLIENT_SECRET = str(os.getenv("EMOTIV_CLIENT_SECRET"))
RESULTS_FOLDER = str(os.getenv("RESULTS_FOLDER"))

app = Flask(__name__,
            static_url_path='', 
            static_folder='.', template_folder="./templates")

current_device = None
worker_thread = None
question_counters = defaultdict(lambda: -1)

def save_results(path):
    df = pd.read_csv("/Users/mkojro/Documents/bachelors-thesis/emotiv-connection/results/Record title_EPOCX_211020_2024.02.14T13.56.26+01.00.md.pm.bp.csv", skiprows=1)
    records = df.to_dict('records')
    # this can be inserted into mongo
    pass

@app.post('/inject_marker')
def inject_marker():
    print("inject_marker_called")
    global current_device
    info = request.json
    App.injcect_marker(current_device.c, info["label"], info["value"])

@app.post('/answers/<id>')
def create_answer(id):
    # Create answert for a given recording and question
    print(request.form)
    global question_counters
    global current_device
    questions = [
            {"question": "Siedz w bezruchu", "answerable": False},
            {"question": "2+2=4", "answerable": True}, 
            {"question": "3+3=12", "answerable": True},
            {"question": "Siedz w bezruchu", "answerable": False},
        ]

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
    App.injcect_marker(current_device.c, id, next_question["question"])
    return render_template("stimuli_form.html", question=next_question["question"], answerable=next_question["answerable"]) 

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
    recording_id = str(uuid4())
    form_values = request.args.to_dict()
    global current_device
    global worker_thread
    del worker_thread
    export_folder = RESULTS_FOLDER + str(recording_id)
    os.makedirs(export_folder, exist_ok=True)
    with open(export_folder + "/metadata.json", "w") as f:
        f.write(json.dumps(form_values))
    current_device = App(
        Cortex(
            client_id=EMOTIV_CLIENT_ID,
            client_secret=EMOTIV_CLIENT_SECRET,
            debug_mode=False,
            url=request.args.get("emotiv_adress")
        ),
        export_folder=export_folder
    )
    worker_thread = Thread(target=current_device.start)
    worker_thread.start()
    return render_template("stimuli.html", id=recording_id)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9090)