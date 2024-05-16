from flask import Flask
from flask import render_template
from flask import jsonify

import nve

app = Flask(__name__)
@app.route("/")
def hello_world():
    name = "Fraktal"
    nve_data = nve.public_mag_data()
    return render_template("index.html", name=name, data=nve_data)
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