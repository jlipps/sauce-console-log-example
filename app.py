#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from flask import Flask, request, render_template
from flask import json

app = Flask(__name__)
app.secret_key = '\t>\x15X\x17\xa7(\xe8\x0f/j\xfe\xb0\xee\xe5\x08\xec\xc8SEZ\x8c\xa2Y'.encode('utf-8')


def render_text(content):
    return app.response_class(content, mimetype='text/plain')


def render_json(content):
    return app.response_class(content, mimetype='application/json; charset=utf-8')


@app.route("/naminatorize", methods=['GET', 'POST'])
def naminatorize():
    text = request.form.get('text') or request.args.get('text')
    if not text:
        return render_json('{}')

    naminatorized = []
    for name in text.split(" "):
        suffix = "nator"
        if name.endswith('e'):
            name = name[:-1] + 'i'
        if not name.endswith(('a', 'i', 'o', 'u', 'y')):
            suffix = 'i' + suffix

        naminatorized.append(name + suffix)
    return render_json(json.dumps(naminatorized))


#@app.route("/naminatorize", methods=['GET', 'POST'])
#def naminatorize():
    #text = request.form.get('text') or request.args.get('text')
    #if not text:
        #return render_json('{}')

    #naminatorized = []
    #for name in text.split(" "):
        #suffix = "nator"
        #did_something_clever = False
        #if name.endswith('e'):
            #name = name[:-1] + 'i'
            #did_something_clever = True
        #if not name.endswith(('a', 'i', 'o', 'u', 'y')):
            #suffix = 'i' + suffix
        #else:
            #did_something_clever = True

        #naminatorized.append({(name + suffix): did_something_clever})
    #return render_json(json.dumps({'result': naminatorized, 'version': '0.1'}))


@app.route("/")
def index():
    return render_template("index.html", **locals())


def main():
    app.run(debug=True, host='0.0.0.0', port=5050)


if __name__ == "__main__":
    main()
