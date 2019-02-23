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
        final = (double(int(result['Budget'])))
        labels = ["January", "February", "March"]
        values = [30,5,3]
        colors = [ "#F7464A", "#46BFBD", "#FDB45C"]

        goal = result['goal']
        print (final)
        print (type(goal))
        return render_template("success.html", data = final, goal = goal, set=zip(values,labels,colors))
if __name__ == '__main__':
    app.run(debug=True)