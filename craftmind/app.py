import logging

from flask import Flask, render_template

from craft import Craft

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', craft=Craft('/home/minecraft'))

@app.route('/users/<username>')
def user(username):
    return render_template('user.html', craft=Craft('/home/minecraft'), username=username)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=52425, debug=True)
