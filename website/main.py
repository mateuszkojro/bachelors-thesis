from dash import Dash, html, callback, Output, Input, dcc, State
import dash_latex as dl
import random
import logging
import time

from mongo_connector import MongoConnection
import platform


MONGO_URI = "mongodb://root:example@rpi.mateuszkojro.com:27017/"
MONGO_DB = "test_db"
MONGO_COLLECTION = "test_collection"

if platform.system() != 'Darwin':
    logging.info("System is not Darwin using decouple")
    from decouple import config
    MONGO_URI = config("MONGO_URL")
    MONGO_DB = config("MONGO_DB")
    MONGO_COLLECTION = config("MONGO_COLLECTION")

INTERVAL_TIME_MS = 10 * 1000

PROMPTS = {"2+2=4": True, "3+3=5": False}
CURRENT_PROMPT = None

ANSWER_YES = "Tak"
ANSWER_NO = "Nie"
ANSWER_EMPTY = "Brak odpowiedzi"

SUBJECT_ID = None

NUM_QUESTIONS = 10

mongo_connector = MongoConnection.from_uri(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
app = Dash(__name__)
server = app.server

questionare_div = html.Div([
    dl.DashLatex("You will see a prompt in a second", id='prompt'),
    html.Div(className="spacer"),
    dcc.RadioItems([ANSWER_YES, ANSWER_NO, ANSWER_EMPTY], ANSWER_EMPTY, inline=False, persistence=False, id='radio'),
    dcc.Interval(id='interval-timer', interval=INTERVAL_TIME_MS, n_intervals=0, max_intervals=NUM_QUESTIONS)
], hidden=True, id='questionare-div')

welcome_div = html.Div([
    dcc.Markdown("Enter subject id below"),
    dcc.Input(id="subject-id-input", type='number'),
    html.Button('Submit', id='submit-button')
], hidden=False, id='welcome-div')

goodbye_div = html.Div([
    dcc.Markdown("Thank you for your answers")
], hidden=True)

app.layout = html.Div(children=[
    html.H1(children="Stimuli generator"),
    welcome_div,
    questionare_div,
    goodbye_div
])

def answer_to_bool(answer):
    if answer == ANSWER_YES:
        return True
    elif answer == ANSWER_NO:
        return False
    return None

@callback(
    [Output('welcome-div', 'hidden'), 
     Output('questionare-div', 'hidden'),
     Output('interval-timer', 'disabled')],
    Input('submit-button', 'n_clicks'),
    State('subject-id-input', 'value'))
def on_submit(n_clicks, subject_id):
    if n_clicks is None:
        return False, True, True
    global SUBJECT_ID
    SUBJECT_ID = subject_id
    logging.info(f"Moving to the questions with {subject_id=}")
    return True, False, False

@callback(
    [Output('prompt', 'children'), Output("radio", "value")],
    Input('interval-timer', 'n_intervals'),
    State('radio', 'value'),
    prevent_initial_call=True)
def on_question_change(n_intervals, input_value):
    global CURRENT_PROMPT
    previous_prompt = CURRENT_PROMPT
    CURRENT_PROMPT = random.choice(list(PROMPTS.keys()))

    if previous_prompt is not None and SUBJECT_ID is not None:
        correct_answer = PROMPTS[previous_prompt]
        mongo_log = {
            "posix_time": time.time_ns(), 
            "subject_id": SUBJECT_ID,
            "question_num": n_intervals,
            "question": previous_prompt,
            "correct_answer": correct_answer,
            "given_answer": answer_to_bool(input_value)
        }
        logging.info(f"Pushing answert to db: {mongo_log}")
        mongo_connector.insert_one(mongo_log)    

    return f"$${CURRENT_PROMPT}$$", ANSWER_EMPTY

if __name__ == '__main__':
    app.run(debug=True)