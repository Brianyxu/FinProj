from flask import Flask, render_template, request
from portfolize import *
import math
import html
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST','GET'])
def success():
    if request.method == 'POST':
        result = request.form
        budget = int(result['Budget'])
        goal = int(result['goal'])
        risk = result['risk']
        label, value = run(budget, goal, risk=='high risk')
        value = value * budget
        for i in label:
            i=html.unescape(i)
        for i in range(len(value)):
            value[i]='%.02f' % (value[i] * budget)
        colors=[]
        for i in range(len(value)):
            colors.append('#%06X' % int(16777215/math.sqrt(i+1)))
        return render_template("success.html", budget = budget, goal = goal, risk = risk, set=zip(value,label, colors))

@app.route('/about')
def about():
    return render_template('about.html')
def helper(a):
    formatted_list = []
    for item in a:
        formatted_list.append("%.2f"%item)
    return (formatted_list)
if __name__ == '__main__':
    app.run(debug=True) 