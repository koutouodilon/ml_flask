from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from joblib import load
import plotly.express as px
import plotly.graph_objects as go
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', href="static/home.svg")
    else:
        text = request.form['text']
        random_string = uuid.uuid4().hex
        path = f"static/{random_string}.svg"
        new_input_np = floats_string_to_np_arr(text)
        model = load('model.joblib')
        make_picture('AgesAndHeights.pkl', model, new_input_np, path)
        return render_template('index.html', href=path)


def make_picture(training_data_filename, model, new_input_np, output_file):
    data = pd.read_pickle(training_data_filename)
    data = data[data['Age'] > 0]
    ages = data['Age']
    heights = data['Height']

    x_new = np.array(list(range(19))).reshape(19, 1)
    preds = model.predict(x_new)

    fig = px.scatter(x=ages, y=heights, title="Height vs Age of People", labels={'x': 'Age (years)',
                                                                                'y': 'Height (inches)'})
    fig.add_trace(go.Scatter(x=x_new.reshape(19), y=preds, mode='lines', name='Model'))

    new_preds = model.predict(new_input_np)
    fig.add_trace(go.Scatter(x=new_input_np.reshape(len(new_input_np)), y=new_preds, mode='markers', name='New Outputs', marker=dict(color='purple', size=20, line=dict(color='purple', width=2))))
    fig.write_image(output_file, width=800, engine="kaleido")
    fig.show()

def floats_string_to_np_arr(floats_str):
    def is_float(inp):
        try:
            float(inp)
            return True
        except:
            return False
    floats = np.array([float(x) for x in floats_str.split(',') if is_float(x)])
    return floats.reshape(len(floats), 1)


