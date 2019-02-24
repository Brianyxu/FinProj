from flask import Flask, render_template, request
from portfolize import *
import math
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
        label, value, roi = run(budget, goal, risk=='high risk')
        value = value * budget
        for i in range(len(value)):
            value[i]='%.02f' % (value[i] * budget)
        colors=[]
        roi = '%.02f' % roi
        for i in range(len(value)):
            colors.append('#%06X' % int(16777215/math.sqrt(i+1)))
        return render_template("success.html", budget = budget, goal = goal, risk = risk, roi = roi, set=zip(value,label, colors))

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
    #port = int(os.environ.get('PORT', 33507))
    #app.run(host='0.0.0.0', port=port)