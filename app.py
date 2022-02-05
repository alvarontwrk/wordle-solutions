#!/usr/bin/env python3

from flask import Flask, jsonify
from wordle_solutions import get_wordle_app, parse_javascript_data

app = Flask(__name__)

js = get_wordle_app()
solutions = parse_javascript_data(js)

@app.route("/")
def get_all_solutions():
    return jsonify(solutions)

@app.route("/<date>")
def get_day_solution(date):
    try:
        return jsonify({date: solutions[date]})
    except:
        return "", 404
