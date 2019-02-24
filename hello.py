from flask import Flask, render_template, request
from model import double
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST','GET'])
def success():
    if request.method == 'POST':
        result = request.form
        budget = (double(int(result['Budget'])))
        labels = ["January", "February", "March"]
        values = [30.385,5.2,33.3]
        colors = [ "#F7464A", "#46BFBD", "#FDB45C"]
        goal = result['goal']
        risk = result['risk']
        return render_template("success.html", budget = budget, goal = goal, risk = risk, set=zip(values,labels,colors))

@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True) 