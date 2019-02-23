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
        print (double(int(result['Budget'])))
        return render_template("success.html", result = result)
if __name__ == '__main__':
    app.run(debug=True)