#!/usr/bin/env python3

from flask import Flask, jsonify
from wordle_solutions import get_wordle_app, parse_javascript_data

app = Flask(__name__)


@app.route("/")
def get_all_solutions():
    js = get_wordle_app()
    solutions = parse_javascript_data(js)
    return jsonify(solutions)

@app.route("/<date>")
def get_day_solution(date):
    js = get_wordle_app()
    solutions = parse_javascript_data(js)
    try:
        return jsonify({date: solutions[date]})
    except:
        return "", 404
