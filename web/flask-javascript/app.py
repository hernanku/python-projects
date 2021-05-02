from flask import Flask, render_template
import os


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/data')
def query():
    return 'Todo...'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

