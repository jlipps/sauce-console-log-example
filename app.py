#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, render_template
from flask import json

app = Flask(__name__)
app.secret_key = '\t>\x15X\x17\xa7(\xe8\x0f/j\xfe\xb0\xee\xe5\x08\xec\xc8SEZ\x8c\xa2Y'


def render_text(content):
    return app.response_class(content, mimetype='text/plain')


def render_json(content):
    return app.response_class(content, mimetype='application/json')


@app.route("/naminatorize", methods=['GET', 'POST'])
def naminatorize():
    text = request.form.get('text') or request.args.get('text')
    if not text:
        return render_json('{}')

    naminatorized = []
    for name in text.split(" "):
        suffix = "nator"
        if not name.endswith(('a', 'e', 'i', 'o', 'u')):
            suffix = "i" + suffix

        naminatorized.append(name + suffix)
    return render_json(json.dumps(naminatorized))


@app.route("/")
def index():
    return render_template("index.html", **locals())


def main():
    app.run(debug=True, host='0.0.0.0', port=5050)


if __name__ == "__main__":
    main()
