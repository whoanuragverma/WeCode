from flask import Flask, render_template
import random
import string

def randomStringDigits(stringLength=6):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<word>')
def main(word):
    return word

@app.route('/add',methods=['GET','POST'])
def add():
    return randomStringDigits()


if __name__ == "__main__":
    app.run(debug=True)
