import logging

from flask import Flask, render_template

from craft import Craft

app = Flask(__name__)

MINECRAFT_DATA_DIR = '/home/minecraft'

@app.route('/')
def root():
    return render_template('index.html', craft=Craft(MINECRAFT_DATA_DIR))

@app.route('/users/<username>')
def user(username):
    return render_template('user.html',
        craft=Craft(MINECRAFT_DATA_DIR),
        usernames=[username],
    )

@app.route('/users/<username>/compare')
def user_comparison_selection(username):
    return render_template('user_comparison_selection.html',
        craft=Craft(MINECRAFT_DATA_DIR),
        username=username,
    )

@app.route('/users/<username>/compare/<othername>')
def user_comparison(username, othername):
    return render_template('user_comparison.html',
        craft=Craft(MINECRAFT_DATA_DIR),
        usernames=[username, othername],
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=52425, debug=True)
