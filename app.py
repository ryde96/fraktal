import pandas as pd
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request, make_response

import frost
import nve

app = Flask(__name__)
@app.route("/")
def hello_world():
    name = "Fraktal"
    nve_data = nve.public_mag_data()
    frost_data = frost.frost_data()

    frost_df = frost.clean_transform_observations(frost.get_observations())
    nve_df = nve.clean_transform_mag_data(
        nve.get_magazine_data('HentOffentligData'))
    df = pd.merge(nve_df, frost_df, on='month')
    json = df.to_json(orient="records")

    return render_template("index.html", name=name, nve=nve_data, frost=frost_data, data=json)
#
# Magazine data
#
@app.route("/mag")
def mag():
    nve_data = nve.public_mag_data()
    print(nve_data)
    return nve_data

@app.route("/mag/el")
def mag_el():
    return "mag/el"

@app.route("/mag/vass")
def mag_vass():
    return "mag/VASS"

@app.route("/frost/observations")
def frost_observations():
    frost_data = frost.frost_data()
    return frost_data

@app.route("/all", methods = ['GET'])
def all():
    omr_type = request.args.get('omr')
    frost_data = frost.clean_transform_observations(frost.get_observations())
    nve_data = nve.clean_transform_mag_data(
        nve.get_magazine_data('HentOffentligData')
        , omr_type)
    df = pd.merge(nve_data, frost_data, on='month')
    r = make_response(df.to_json(orient="records"))
    r.mimetype = 'application/json'
    return r

@app.route("/csv", methods = ['GET'])
def csv():

    omr_type = request.args.get('omr')
    if omr_type is None:
        omr_type = ''
    frost_data = frost.clean_transform_observations(frost.get_observations())
    nve_data = nve.clean_transform_mag_data(
        nve.get_magazine_data('HentOffentligData')
        , omr_type)
    df = pd.merge(nve_data, frost_data, on='month')
    r = make_response(df.to_csv())
    r.mimetype = 'text/csv'
    return r



